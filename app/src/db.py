from motor import motor_asyncio
import datetime
import typing

# I want separate class to me able to change DB from mongo
class dbHelper:
    """Class to connect to db."""
    def __init__(self, addr: str, db_name: str='app', collection_name: str='secrets') -> None:
        """Creates dbHelper"""
        self.MAX_POOL_SIZE = 10
        self.client = motor_asyncio.AsyncIOMotorClient(addr, maxPoolSize=self.MAX_POOL_SIZE)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.collection.create_index('expires_at', expireAfterSeconds=1)

    async def insert(self, key: str, enc: str, salt: str, ttl: typing.Optional[int] = None) -> typing.Awaitable[None]:
        """Insert document into collection."""
        if ttl is None:
            await self.collection.insert_one({
                'secret_key': key,
                'enc': enc,
                'salt': salt,
            })
        else:
            await self.collection.insert_one({
                'secret_key': key,
                'enc': enc,
                'salt': salt,
                'expires_at': datetime.datetime.utcnow() + datetime.timedelta(seconds=ttl),
            })


    async def remove(self, key: str) -> typing.Awaitable[None]:
        """Removes document from collection."""
        await self.collection.delete_one({
            'secret_key': key,
        })

    async def find(self, key: str) -> typing.Awaitable[typing.Optional[typing.Tuple[str, str]]]:
        """Finds document in collection."""
        result = await self.collection.find_one({
            'secret_key': key,
        })
        if not result:
            return None
        expires_at = result.get('expires_at', None)
        if expires_at is not None and datetime.datetime.utcnow() > expires_at:
            return None
        return result['enc'], result['salt']
