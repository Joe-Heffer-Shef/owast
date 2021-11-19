import os

import pymodm.connection

CONNECTION_STRING = os.environ['MONGO_URI']


def main():
    conn = pymodm.connection.connect(CONNECTION_STRING)
    print(repr(conn))
