# coding: utf-8

import os
import base64
import csv
from argparse import ArgumentParser

def create_new_file(chunks_dir, file_counter, fieldnames):
    new_file = os.path.join(chunks_dir, "chunk_%d.csv" % file_counter)
    with open(new_file, 'w+') as chunk:
        writer = csv.DictWriter(chunk, fieldnames=fieldnames)
        writer.writeheader()
    file_counter += 1
    return new_file,file_counter

def main(values):

    if not os.path.isfile(values.file_location) or os.stat(values.file_location).st_size == 0:
        print("Plz check for given file may be its empty or not exist.")
        return 1

    chunks_dir = os.path.join(os.getcwd(),'file_chunks')
    if not os.path.isdir(chunks_dir):
        os.makedirs(chunks_dir)

    file_counter = 1
    record_conter = values.limit
    with open(values.file_location, 'r') as readFile:
        filedata = csv.DictReader(readFile)
        for row in filedata:
            if record_conter == values.limit:
                new_file,file_counter = create_new_file(chunks_dir, file_counter, filedata.fieldnames)
                chunk_write = open(new_file, 'w')
                write_data = csv.DictWriter(chunk_write, fieldnames=filedata.fieldnames)
                write_data.writeheader()
                record_conter = 0
            write_data.writerow(row)
            record_conter += 1

if __name__ == '__main__':
    op = ArgumentParser(description='Process some CSV files operations.')
    op.add_argument("-f", "--file-location", action="store",
                    help="Location Of Directory Where You Been Put Your Files")
    op.add_argument("-l", "--limit", default=100, action="store",
                    type=int, help="Total number of records per file")
    values = op.parse_args()
    main(values)
