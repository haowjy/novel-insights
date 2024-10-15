# db.py
# Description: Define the database structure, embedding model, and methods to interact with the database.

from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams

# from llama_index.core.base.embeddings.base import BaseEmbedding
from fastembed import TextEmbedding

from novelinsights.config import Config

config = Config()

class Collection(BaseModel):        
    collection_name: str
    embedding_model: TextEmbedding
    vectors_config: VectorParams
    
    class Config:
        arbitrary_types_allowed = True

class Collections(BaseModel):
    
    FictionWikiGenCollection: Collection
    
    class Config:
        arbitrary_types_allowed = True
    
class QdrantDB:
    def __init__(self):
        self.client: QdrantClient = None
        self.collections: Collections = None
        self.initialize_db()
    
    def connect(self):
        self.client = QdrantClient(url=config.QDRANT_URL)
    
    def initialize_db(self):
        if self.client is None:
            self.connect()
        
        fiction_wikigen_collection = Collection(
            collection_name='FictionWikiGen',
            embedding_model=TextEmbedding('BAAI/bge-small-en-v1.5'),
            vectors_config=VectorParams(
                size=384,
                distance='Cosine',
            )
        )
        self.collections = Collections(
            FictionWikiGenCollection=fiction_wikigen_collection
        )
        
        # for each of the keys in self.collections, create a collection in the database if it doesn't already exist
        for _, val in iter(self.collections):
            if not self.client.collection_exists(collection_name=val.collection_name):
                self.client.create_collection(
                    collection_name=val.collection_name,
                    vectors_config=val.vectors_config
                )
