import datetime
import time

from domain.GrowingTile import GrowingTile
import sqlite3


class TileGrowthDao:

    def __init__(self):
        self.SQL_LITE_FILE_PATH = "C:\\Licenta\\Licenta\\resources\\sqlLite\\db.sqlite"

        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS GrowingTile ('
                       ' global_i INTEGER NOT NULL,'
                       ' global_j INTEGER NOT NULL,'
                       ' tile_code INTEGER NOT NULL,'
                       ' created_timestamp INTEGER NOT NULL,'
                       ' PRIMARY KEY (global_i, global_j)'
                       ');')


        self.commit_and_close(connection)

        file_path = "C:\\Licenta\\Licenta\\resources\\WorldMap\\50-50-chunk.txt"

        try:
            with open(file_path):
                pass
        except OSError:
            self.clear_table()



    def get_connection(self):
        return sqlite3.connect(self.SQL_LITE_FILE_PATH)

    def commit_and_close(self, connection):
        connection.commit()
        connection.close()

    def insert_growing_tile(self, global_pos, tile_code):
        # :param: global_pos - global i and j (i, j) will be used as pk

        created_timestamp = int(round(time.time() * 1000))
        connection = self.get_connection()
        cursor = connection.cursor()


        cursor.execute("INSERT INTO GrowingTile "
                       "(global_i, global_j, tile_code, created_timestamp)"
                       "VALUES"
                       "(?, ?, ?, ?)",
                       (global_pos[0], global_pos[1], tile_code, created_timestamp)
                       )

        self.commit_and_close(connection)

    def batch_insert(self, growing_tiles_batch):

        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.executemany("INSERT INTO GrowingTile "
                       "(global_i, global_j, tile_code, created_timestamp)"
                       "VALUES"
                       "(?, ?, ?, ?)",
                       growing_tiles_batch
                       )

        self.commit_and_close(connection)



    def get_growing_tile(self, global_pos):

        connection = self.get_connection()

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM GrowingTile "
                       "WHERE global_i = ? AND global_j = ?",
                       (global_pos[0], global_pos[1]))

        rows = cursor.fetchall()

        growing_tile_tuple = rows[0]
        growing_tile = self.map_object(growing_tile_tuple)

        self.commit_and_close(connection)

        return growing_tile

    def delete_growing_tile(self, global_pos):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("DELETE FROM GrowingTile "
                       "WHERE global_i = ? AND global_j = ?",
                       (global_pos[0], global_pos[1]))
        self.commit_and_close(connection)


    # TODO figure out a way to have multiple worlds
    def clear_table(self):

        connection = self.get_connection()

        cursor = connection.cursor()
        cursor.execute("DELETE FROM GrowingTile")

        self.commit_and_close(connection)


    def map_object(self, sqlite_tuple):

        global_i = sqlite_tuple[0]
        global_j = sqlite_tuple[1]
        tile_code = str(sqlite_tuple[2])
        created_timestamp = datetime.datetime.fromtimestamp(sqlite_tuple[3] / 1000.0)

        return GrowingTile((global_i, global_j), tile_code, created_timestamp)


