import pymongo
from motor import motor_asyncio
import typing

# TODO: set index?

# I want separate class to me able to change DB from mongo
class dbHelper:
    """Class to connect to db"""
    def __init__(self, db_name: str='app', collection_name: str='secrets', addr: str='db') -> None:
        """Creates dbHelper"""
        self.MAX_POOL_SIZE = 10
        self.client = motor_asyncio.AsyncIOMotorClient(addr, maxPoolSize=self.MAX_POOL_SIZE)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    async def insert(self, key: str, enc: str, salt: str) -> typing.Awaitable[None]:
        """Insert document into collection"""
        await self.collection.insert_one({
            'secret_key': key,
            'enc': enc,
            'salt': salt,
        })

    async def remove(self, key: str) -> typing.Awaitable[None]:
        """Removes document from collection"""
        await self.collection.delete_one({
            'secret_key': key,
        })

    async def find(self, key: str) -> typing.Awaitable[typing.Optional[typing.Tuple[str, str]]]:
        """Finds document in collection"""
        result = await self.collection.find_one({
            'secret_key': key,
        })
        if not result:
            return None
        return result['enc'], result['salt']
