#!/usr/bin/env python3
"""
Module for changing topics
"""


def update_topics(mongo_collection, name, topics):
    """
    A function that changes all topics of a school doc based on a ame
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
