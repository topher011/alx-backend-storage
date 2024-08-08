#!/usr/bin/env python3
'''
 a Python script that provides some stats about Nginx logs stored in MongoDB
'''
from pymongo import MongoClient


def log_summary():
    '''
    prints a summary of nginx log
    '''
    client = MongoClient()
    nginx_collection = client.logs.nginx
    no_logs = nginx_collection.count_documents({})
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("{} logs".format(no_logs))
    print("Methods:")
    for mthd in methods:
        print("\tmethod {}: {}".format(mthd, nginx_collection.count_documents(
            {"method": mthd}
        )))
    print("{} status check".format(nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )))


if __name__ == "__main__":
    log_summary()
