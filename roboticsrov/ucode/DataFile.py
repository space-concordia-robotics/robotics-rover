import csv

class DataFile:

    def __init__(self, output_path):
        self.file_handle = open(output_path, 'wb')
        self.writer = csv.writer(self.file_handle)

    def write_header(self, header_iterable):
        self.writer.writerow(header_iterable)

    def write_single_row(self, row_iterable):
        self.writer.writerow(row_iterable)

    def write_array(self, array_iterable):
        self.writer.writerows(array_iterable)

    def close_file(self):
        self.file_handle.close()
