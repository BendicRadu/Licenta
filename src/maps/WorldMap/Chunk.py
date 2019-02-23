import csv
import datetime
import random

from util import Constants


class Chunk:

    def __init__(self, offset_i, offset_j):

        self.offset_i = offset_i
        self.offset_j = offset_j

        self.matrix = []

        if self.is_chunk_generated():
            self.load_chunk()
        else:
            self.generate_chunk()


    def is_chunk_generated(self):

        file_path = "C:\\Licenta\\Licenta\\resources\\WorldMap\\" \
                    + str(self.offset_i) + "-" + str(self.offset_j) + "-chunk.txt"

        try:
            with open(file_path):
                return True

        except OSError:
            return False


    def load_chunk(self):

        file_path = "C:\\Licenta\\Licenta\\resources\\WorldMap\\" \
                    + str(self.offset_i) + "-" + str(self.offset_j) + "-chunk.txt"

        with open(file_path, "r") as file:
            for line in file:
                self.matrix.append(line.strip("\n").split(","))



    def generate_chunk(self):

        for i in range(Constants.CHUNK_SIZE):

            matrix_row = []

            for j in range(Constants.CHUNK_SIZE):
                random_index = random.randint(0, len(Constants.SPAWN_CHANCE_LIST) - 1)
                object_type = Constants.SPAWN_CHANCE_LIST[random_index]

                matrix_row.append(object_type)

            self.matrix.append(matrix_row)

        self.save_chunk()


    def save_chunk(self):

        file_path = "C:\\Licenta\\Licenta\\resources\\WorldMap\\"
        file_path += str(self.offset_i) + "-" + str(self.offset_j) + "-chunk.txt"

        file = open(file_path, "w+", newline='')

        for row in self.matrix:
            wr = csv.writer(file)
            wr.writerow(row)


    def get_tile(self, pos_tuple):
        return self.matrix[pos_tuple[0]][pos_tuple[1]]

