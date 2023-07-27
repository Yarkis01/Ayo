from enum import Enum

from motor.motor_asyncio import AsyncIOMotorClient
#from pymongo.server_api  import ServerApi
import pymongo

from utils.logger import Logger

class Collections(Enum):
    """An enum representing the collection names."""
    FRIEND_CODES = "friendCodes"
    GUILDS       = "guilds"
    ROTATIONS    = "rotations"
    SPLAT        = "splat"

class Database:
    """A class to interact with a MongoDB database."""  

    def __init__(self, mongo_uri: str):
        """
        Initialize the database client and database name.
        
        Args:
            mongo_uri (str): The MongoDB URI.
        """
        Logger.info("Attempting to connect to the database...", "database")
        # For some obscure reason, forced to do it this way...
        #self.__client   = AsyncIOMotorClient(mongo_uri, server_api = ServerApi('1'))
        self.__client   = AsyncIOMotorClient(mongo_uri)
        self.__database = self.__client.AyoDatabase
        Logger.success("Successful database connection", "database")

    async def init_collection(self, collection: Collections) -> None:
        """
        Ensure an index exists on the createdAt field for the collection.
        
        Args:
            collection (Collections): The collection enum. 
        """
        collection = self.__database[collection.value]

        if not await collection.index_information():
            await collection.create_index([
                ("createdAt", pymongo.ASCENDING)
            ])
            
    async def find_documents(self, collection: Collections, query: dict) -> list:
        """
        Find documents from a collection.
        
        Args: 
            collection (Collections): The collection enum.
            query (dict): The query dict.
            
        Returns:
            List[dict]: The documents.
        """

        collection = self.__database[collection.value]
        return await collection.find(query).to_list(length = None)
    
    async def find_one(self, collection: Collections, query: dict) -> dict:
        """
        Find one document matching the query.

        Args:
            collection (Collections): The collection enum
            query (dict): The query filter
            
        Returns:
            dict: The matching document
        """

        docs = await self.find_documents(collection, query) 
        return docs[0] if docs else None
    
    async def insert_document(self, collection: Collections, document: dict) -> str:
        """
        Insert a document to a collection.
        
        Args:
            collection (Collections): The collection enum.
            document (dict): The document to insert.
            
        Returns:
            str: The inserted ID.    
        """

        collection = self.__database[collection.value]
        result     = await collection.insert_one(document)
        return result.inserted_id
    
    async def delete_document(self, collection: Collections, query: dict) -> int:
        """
        Delete a document from a collection.

        Args:
            collection (Collections): The collection enum.
            query (dict): The filter to find the document to delete.
        """
        
        collection = self.__database[collection.value]
        await collection.delete_one(query)
    
    async def update_document(self, collection: Collections, query: dict, update: dict) -> None:
        """
        Update a document in a collection.
        
        Args:
            collection (Collections): The collection enum.
            query (dict): The filter to find the document to update.
            update (dict): The update operations.
        """
        
        collection = self.__database[collection.value]
        await collection.update_one(query, {'$set': update})
        
    async def count_documents(self, collection: Collections) -> int:
        """
        Get the number of documents in a collection.

        Args:
            collection (Collections): The collection enum.

        Returns: 
            int: The number of documents.
        """

        collection = self.__database[collection.value]
        return await collection.estimated_document_count()