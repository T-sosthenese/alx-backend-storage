#!/usr/bin/env python3
"""
A module that returns all documents in a collection
"""


def list_all(mongo_collection):
    """
    Returns all documents in a collection
    """
    return list(mongo_collection.find())
