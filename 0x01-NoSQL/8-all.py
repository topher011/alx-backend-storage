#!/usr/bin/env python3
'''
a Python function that lists all documents in a collection
'''


def list_all(mongo_collection):
    '''
    function lists all documents in a collection
    Args:
        - mongo_collection - the pymongo collection
    '''
    return mongo_collection.find()
