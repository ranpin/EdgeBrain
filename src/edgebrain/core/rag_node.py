import os
from typing import List, Optional
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.core.embeddings.mock_embed_model import MockEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from loguru import logger

class RAGNode:
    """
    EdgeBrain RAG 检索节点
    负责文档加载、向量化及语义检索
    """
    def __init__(self, data_dir: str = "./data", persist_dir: str = "./storage"):
        self.data_dir = data_dir
        self.persist_dir = persist_dir
        self.index = None
        self._init_chroma()

    def _init_chroma(self):
        """初始化 ChromaDB 向量存储"""
        try:
            logger.info(f"Initializing RAG with data_dir: {self.data_dir}")
            
            # 配置本地 Embedding 模型 (端侧适配：使用 MockEmbedding 规避 PyTorch 冲突)
            # 在实际部署到 Orin/8397 时，可替换为 QNN 加速的 ONNX Embedding 模型
            Settings.embed_model = MockEmbedding(embed_dim=1536)
            
            db = chromadb.PersistentClient(path=self.persist_dir)
            chroma_collection = db.get_or_create_collection("edgebrain_knowledge")
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            
            # 检查目录并加载文档
            if os.path.exists(self.data_dir):
                files = os.listdir(self.data_dir)
                logger.info(f"Files found in data_dir: {files}")
                if files:
                    documents = SimpleDirectoryReader(self.data_dir, recursive=True).load_data()
                    if documents:
                        self.index = VectorStoreIndex.from_documents(
                            documents, 
                            storage_context=storage_context
                        )
                        logger.info(f"RAG Index initialized with {len(documents)} documents.")
                    else:
                        logger.warning("No valid documents loaded by SimpleDirectoryReader.")
                else:
                    logger.warning("Data directory exists but is empty.")
            else:
                logger.warning(f"Data directory does not exist: {self.data_dir}")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")

    def query(self, question: str, top_k: int = 3) -> List[str]:
        """执行语义检索"""
        if not self.index:
            return []
        
        try:
            query_engine = self.index.as_query_engine(similarity_top_k=top_k)
            response = query_engine.query(question)
            return [node.text for node in response.source_nodes]
        except Exception as e:
            logger.error(f"RAG query failed: {e}")
            return []
