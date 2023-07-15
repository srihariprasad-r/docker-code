import os, csv
from prepareCustomfiles import preparefiles
import argparse
import json

class fileHandler(preparefiles):
    def __init__(self, filepath, filetype, delimited=',', hdfs_connection='',aws_connection=''):
        self.filepath = filepath
        self.filetype = filetype
        self.delimited = delimited
        self.filename = 'customers.csv' if self.file_type == 'csv' else None
        self.targetencryptfilename = None
        self.csvencryptedentries = []
        super(fileHandler, self).__init__(filepath, filetype, delimited)
        
    def prepare_file(self):
        return self.prepare_csv_file(self.filename)
    
    def parse_config_fields(self, file):
        with open(file, 'r') as f:
            file_contents = f.read()

        entries = json.loads(file_contents)
        encrypted_fields_list = dict()

        for k, v in entries.items():
            for i in range(len(v)):
                if v[i]['source_file_name'] == self.filename:
                    self.targetencryptfilename = v[i]['target_file_name']
                    for k, v in v[i]['fields'].items():
                        encrypted_fields_list[k] = v

        return encrypted_fields_list
    
    def encryptfiles(self):
        fields = self.parse_config_fields('fileconfig.json')
        if self.file_type == 'csv':
            with open(os.path.join(self.filepath, self.filename), 'r', newline='') as file:
                reader = csv.DictReader(file, delimiter=self.delimited)
                self.csvencryptedentries.append(reader.fieldnames)
                for row in reader:
                    col_vals = []
                    for _, v in row.items():
                        col_vals.append(v)
                    self.csvencryptedentries.append(col_vals)

        return self.csvencryptedentries

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filetype', type=str, required=True)
    parser.add_argument('--filepath', type=str, required=True)
    parser.add_argument('--csvdelimiter', type=str)
    args = parser.parse_args()

    filehandler_object = fileHandler(args.filepath, args.filetype, args.csvdelimiter)
    filehandler_object.prepare_file()
