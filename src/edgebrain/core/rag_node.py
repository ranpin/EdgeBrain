import os
import requests
from typing import List, Optional
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings, Document
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from loguru import logger
from src.edgebrain.config import (
    OLLAMA_URL, 
    LLM_MODEL_NAME, 
    EMBEDDING_MODEL_NAME, 
    CHROMA_PERSIST_DIR, 
    KNOWLEDGE_BASE_DIR
)

class RAGNode:
    """
    EdgeBrain RAG 检索节点
    支持 Ollama 在线模式与本地离线回退模式
    """
    def __init__(self, data_dir: str = KNOWLEDGE_BASE_DIR, persist_dir: str = CHROMA_PERSIST_DIR):
        self.data_dir = data_dir
        self.persist_dir = persist_dir
        self.model_name = model_name
        self.index = None
        self._init_chroma()

    def _check_ollama(self) -> bool:
        """检查 Ollama 服务是否可达"""
        try:
            requests.get("http://localhost:11434/api/tags", timeout=2)
            return True
        except:
            return False

    def _init_chroma(self):
        """初始化 ChromaDB 向量存储"""
        try:
            logger.info(f"Initializing RAG with data_dir: {self.data_dir}")
            
            # 尝试使用 Ollama，失败则回退到 Mock/本地模式
            if self._check_ollama():
                from llama_index.llms.ollama import Ollama
                from llama_index.embeddings.ollama import OllamaEmbedding
                # 使用真实的 Embedding 模型和 LLM
                Settings.embed_model = OllamaEmbedding(model_name=EMBEDDING_MODEL_NAME)
                Settings.llm = Ollama(model=LLM_MODEL_NAME, request_timeout=120.0)
                logger.info(f"RAG Mode: Ollama Online (LLM: {LLM_MODEL_NAME}, Embed: {EMBEDDING_MODEL_NAME})")
            else:
                logger.warning("Ollama not accessible. Falling back to offline mode.")
                from llama_index.core.embeddings import MockEmbedding
                # 确保 MockEmbedding 的维度与 ChromaDB 集合预期一致 (1536)
                Settings.embed_model = MockEmbedding(embed_dim=1536)
                Settings.llm = None 
                logger.info("RAG Mode: Offline (MockEmbedding 1536-dim)")

            db = chromadb.PersistentClient(path=self.persist_dir)
            collection_name = "edgebrain_knowledge"
            
            # 强制删除旧集合并重新创建，确保维度与当前 Embedding 模型一致
            current_dim = Settings.embed_model.embed_dim if hasattr(Settings.embed_model, 'embed_dim') else 768
            try:
                db.delete_collection(collection_name)
            except:
                pass
            
            chroma_collection = db.create_collection(
                collection_name, 
                metadata={"hnsw:space": "cosine", "dimension": current_dim}
            )
            logger.info(f"Created fresh collection '{collection_name}' with dimension {current_dim}")

            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            
            if os.path.exists(self.data_dir):
                documents = SimpleDirectoryReader(self.data_dir, recursive=True).load_data()
                if documents:
                    self.index = VectorStoreIndex.from_documents(
                        documents, 
                        storage_context=storage_context
                    )
                    logger.info(f"RAG Index initialized with {len(documents)} documents.")
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