# db.py
# Description: Define the database structure, embedding model, and methods to interact with the database.

from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, TextIndexParams, TokenizerType, KeywordIndexParams

# from llama_index.core.base.embeddings.base import BaseEmbedding
from fastembed import TextEmbedding

from novelinsights.config import Config

config = Config()

class Collection(BaseModel):        
    name: str
    embed_model: TextEmbedding
    vectors_config: dict[str, VectorParams]
    
    class Config:
        arbitrary_types_allowed = True
    
class QdrantDB:
    def __init__(self):
        self.client: QdrantClient = None
        
        self.fiction_wikigen: Collection = None
        self.book_list: Collection = None
        
        self.initialize_db()
    
    def connect(self):
        self.client = QdrantClient(url=config.QDRANT_URL)
    
    def initialize_db(self):
        if self.client is None:
            self.connect()
        
        self.fiction_wikigen = Collection(
            name='FictionWikiGen',
            embed_model=TextEmbedding('BAAI/bge-small-en-v1.5'),
            vectors_config={
                "bge-small-en-v1.5":VectorParams(
                size=384,
                distance='Cosine',
            )}
        )
        self._create_fiction_wikigen(self.fiction_wikigen)
        
        self.book_list = Collection(
            name='BookList',
            embed_model=TextEmbedding('BAAI/bge-small-en-v1.5'),
            vectors_config={
                "bge-small-en-v1.5":VectorParams(
                size=384,
                distance='Cosine',
            )}
        )

        # for each of the keys in self.collections, create a collection in the database if it doesn't already exist
            
    def _create_fiction_wikigen(self, collection: Collection):
        if not self.client.collection_exists(collection_name=collection.name):
            self.client.create_collection(
                collection_name=collection.name,
                vectors_config=collection.vectors_config
            )
            
            # UUID of the book
            self.client.create_payload_index(
                collection_name=collection.name,
                field_name='book_uuid',
                field_schema=KeywordIndexParams(
                type="uuid",
                is_tenant=True,
            ))
            
            # Name
            self.client.create_payload_index(
                collection_name=collection.name,
                field_name='name',
                field_schema=TextIndexParams(
                    type="text",
                    tokenizer=TokenizerType.WORD,
                    min_token_len=2,
                    max_token_len=15,
                    lowercase=True,
                ))
            
            # Alias
            self.client.create_payload_index(
                collection_name=collection.name,
                field_name='alias',
                field_schema=TextIndexParams(
                    type="text",
                    tokenizer=TokenizerType.WORD,
                    min_token_len=2,
                    max_token_len=15,
                    lowercase=True,
                ))
            
            # Chapter Number - ONLY FOR CHAPTER CHRONOLOGY
            self.client.create_payload_index( 
                collection_name=collection.name,
                field_name='chap_num',
                field_schema='integer',
            )
    
    def _create_book_list(self, collection: Collection):
        if not self.client.collection_exists(collection_name=collection.name):
            self.client.create_collection(
                collection_name=collection.name,
                vectors_config=collection.vectors_config
            )
            
            # Book Title
            self.client.create_payload_index(
                collection_name=collection.name,
                field_name='name',
                field_schema=KeywordIndexParams(
                type="keyword",
                is_tenant=True,
            ))
            
            # Author
            self.client.create_payload_index(
                collection_name=collection.name,
                field_name='author',
                field_schema=TextIndexParams(
                    type="text",
                    tokenizer=TokenizerType.WORD,
                    min_token_len=2,
                    max_token_len=15,
                    lowercase=True,
                ),
            )