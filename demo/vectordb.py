# just playing around with a pgvector database + embeddings

import psycopg2
from typing import List, Tuple

class PGVectorDB():
    def __init__(self, config):
        conn = psycopg2.connect(database=config.db_name,
                                host=config.db_host,
                                user=config.user,
                                password=config.password,
                                port=config.db_port
                                )
        cursor = conn.cursor()
        cursor.execute("CREATE EXTENSION VECTOR")