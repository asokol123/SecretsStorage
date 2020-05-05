import pymongo
import typing

# TODO: set index?

# I want separate class to me able to change DB from mongo
class dbHelper:
    """Class to connect to db"""
    def __init__(self, db_name: str='app', collection_name: str='secrets', addr: str='db') -> None:
        """Creates dbHelper"""
        self.client = pymongo.MongoClient(addr)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert(self, key: str, enc: str, iv: str) -> None:
        """Insert document into collection"""
        self.collection.insert_one({
            'secret_key': key,
            'enc': enc,
            'iv': iv,
        })

    def remove(self, key: str) -> None:
        """Removes document from collection"""
        self.collection.delete_one({
            'secret_key': key,
        })

    def find(self, key: str) -> typing.Optional[typing.Tuple[str, str]]:
        """Finds document in collection"""
        result = self.collection.find_one({
            'secret_key': key,
        })
        if not result:
            return None
        return result['enc'], result['iv']
