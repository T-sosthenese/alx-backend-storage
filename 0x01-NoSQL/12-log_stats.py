#!/usr/bin/env python3
"""
Module implementation
"""

from pymongo import MongoClient


if __name__ == "__main__":
    """
    Provides stats about nginx logs
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    coll = client.logs.nginx
    print("{} logs".format(coll.count_documents({})))
    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = coll.count_documents({'method': method})
        print("\tmethod {}: {}".format(method, count))

    status_get = coll.count_documents({'method': 'GET', 'path': "/status"})
    print("{} status check".format(status_get))
