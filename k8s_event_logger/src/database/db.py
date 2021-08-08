import os

import pymongo.errors
from pymongo import MongoClient

try:
    from database import events
except ImportError:
    # when creating the index our sys.path will contain dir(database/db.py) instead of dir(k8s_asyncio.py)
    import events

client = MongoClient(username=os.environ.get('MONGO_USERNAME', 'root'),
                     password=os.environ.get('MONGO_PASSWORD', 'example'))
DB = client['k8s_events']
print(DB)


def _create_indexes(collections):
    for collection in collections:
        DB[collection].create_index('raw_object.metadata.resourceVersion', unique=True)


def insert_k8s_event(obj_type: str, raw_obj: dict, event_type: str):
    collection = DB[obj_type]

    try:
        obj_id = collection.insert_one(dict(event_type=event_type,
                                            raw_object=raw_obj)).inserted_id
        print(obj_id)
    except pymongo.errors.DuplicateKeyError:
        print('skipping')


if __name__ == '__main__':
    _create_indexes(event for event in dir(events) if event.endswith('_EVENT'))
