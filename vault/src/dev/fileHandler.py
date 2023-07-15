import os, csv
from prepareCustomfiles import preparefiles
from app import hvacClient
import json

class fileHandler(preparefiles, hvacClient):
    def __init__(self, hdfs_connection='', aws_connection='', **params):
        self.filepath = params['filepath']
        self.filetype = params['filetype']
        self.delimited = params['csvdelimiter']
        self.filename = 'customers.csv' if self.filetype == 'csv' else None
        self.targetencryptfilename = None
        self.csvencryptedentries = []
        super(fileHandler, self).__init__(self.filepath, self.filetype, self.delimited)
        
    def prepare_file(self, filename='', entries=''):
        return self.prepare_csv_file(filename, entries)
    
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
    
    def encryptfiles(self, conf):
        fields = self.parse_config_fields('fileconfig.json')
        if self.file_type == 'csv':
            with open(os.path.join(self.filepath, self.filename), 'r', newline='') as file:
                reader = csv.DictReader(file, delimiter=self.delimited)
                self.csvencryptedentries.append(reader.fieldnames)
                for row in reader:
                    col_vals = []
                    for k , v in row.items():
                        if k in fields:
                            v = super(fileHandler, self)._encrypt_non_ssn_ccn(v, conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])
                        col_vals.append(v)
                    self.csvencryptedentries.append(col_vals)

        return self.csvencryptedentries
    
    def removefile(self, filepath, filename):
        os.remove(os.path.join(filepath, filename))

