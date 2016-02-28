# -*- coding: utf-8 -*-
from pymongo import MongoClient


def get_db_connection():
        client = MongoClient()
        return client
