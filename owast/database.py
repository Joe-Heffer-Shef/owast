import pymongo


def get_db() -> pymongo.database.Database:
    """
    Load the PyMongo database handle
    """
    client = pymongo.MongoClient('meta')
    db = client.owast

    return db
