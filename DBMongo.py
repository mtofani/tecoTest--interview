# Mongopy wrapper

import pymongo


class DBMongo(object):

    def __init__(self, url, BD):

        self.client = pymongo.MongoClient(
            url, serverSelectionTimeoutMS=6000)
        self.db = self.client[BD]

    def cerrarMongo(self):
        self.client.close()
