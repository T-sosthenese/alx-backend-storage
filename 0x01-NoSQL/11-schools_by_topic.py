#!/usr/bin/env python3
"""
Module that changes topics
"""


def schools_by_topic(mongo_collection, topic):
    """
    Function that changes the topics of certain docs based on their names
    """
    return mongo_collection.find({"topics": topic})
