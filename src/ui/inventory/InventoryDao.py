import datetime
import time

from domain.GrowingTile import GrowingTile
import sqlite3

from ui.inventory.ItemStack import ItemStack
from util.GameVars import BASE_PATH


class InventoryDao:

    SQL_LITE_FILE_PATH = BASE_PATH + "resources\\sqlLite\\db.sqlite"

    def __init__(self):

        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS ItemStack ('
                       ' tile_code INTEGER NOT NULL,'
                       ' quantity INTEGER NOT NULL,'
                       ' inventory_i INTEGER NOT NULL,'
                       ' inventory_j INTEGER NOT NULL,'
                       ' PRIMARY KEY(inventory_i, inventory_j)'
                       ');')

        CONVENIENT_PATH = BASE_PATH + "resources\\WorldMap\\50-50-chunk.txt"

        try:
            with open(CONVENIENT_PATH):
                pass
        except OSError:
            self.clear_table()

        self.commit_and_close(connection)




    def get_connection(self):
        return sqlite3.connect(self.SQL_LITE_FILE_PATH)

    def commit_and_close(self, connection):
        connection.commit()
        connection.close()

    def batch_insert(self, item_stack_batch):

        connection = self.get_connection()
        cursor = connection.cursor()

        cursor.executemany("INSERT INTO ItemStack "
                       "(tile_code, quantity, inventory_i, inventory_j)"
                       "VALUES"
                       "(?, ?, ?, ?)",
                       item_stack_batch
                       )

        self.commit_and_close(connection)



    def get_all_items(self):

        connection = self.get_connection()

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ItemStack ")

        rows = cursor.fetchall()
        result = list(map(self.map_object, rows))
        self.commit_and_close(connection)

        return result

    def clear_table(self):

        connection = self.get_connection()

        cursor = connection.cursor()
        cursor.execute("DELETE FROM ItemStack")

        self.commit_and_close(connection)


    def map_object(self, sqlite_tuple):

        tile_code = sqlite_tuple[0]
        quantity = sqlite_tuple[1]
        inventory_i = sqlite_tuple[2]
        inventory_j = sqlite_tuple[3]

        return ItemStack(str(tile_code), quantity, inventory_i = inventory_i, inventory_j = inventory_j)


