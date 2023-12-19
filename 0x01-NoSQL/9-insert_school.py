#!/usr/bin/env python3
"""
A module that adds a document to a collection.
"""


def insert_school(mongo_collection, **kwargs):
    """
    A function that adds a document to a collection
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
