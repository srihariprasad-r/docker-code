import os, csv
from prepareCustomfiles import preparefiles
from app import hvacClient
import json

class fileHandler(preparefiles, hvacClient):
    def __init__(self, hdfs_connection='', aws_connection='', **params):
        self.filepath = params['filepath']
        self.filetype = params['filetype']
        self.delimited = params['csvdelimiter']
        self.filename = 'customers.csv' if self.filetype == 'csv' else 'jsoncustomers.json'
        self.targetencryptfilename = None
        self.csvencryptedentries = []
        super(fileHandler, self).__init__(self.filepath, self.filetype, self.delimited)
        
    def prepare_file(self, filename='', entries='', flag=False):
        if self.file_type == 'csv':
            return self.prepare_csv_file(filename, entries)
        if self.file_type == 'json':
            if not flag:
                return self.prepare_json_file(filename, self.jsonschema, self.jsonentries)
            else:
                return self.prepare_json_file(filename, entries=entries)
    
    def parse_config_fields(self, file):
        with open(file, 'r') as f:
            file_contents = f.read()

        entries = json.loads(file_contents)
        encrypted_fields_list = dict()

        for k, v in entries.items():
            for i in range(len(v)):
                if v[i]['source_file_name'] == self.filename:
                    self.targetencryptfilename = v[i]['target_file_name']
                    for m, n in v[i]['fields'].items():
                        encrypted_fields_list[m] = n

        return encrypted_fields_list
    
    def encryptfiles(self, conf):
        fields = self.parse_config_fields('fileconfig.json')
        # csv processing
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
        # json processing
        if self.file_type == 'json':
            output = []
            with open(os.path.join(self.filepath, self.filename), 'r', newline='') as file:
                file_contents = file.read()

            entries = json.loads(file_contents)

            for el in entries:
                tmp = {}
                for k, v in el.items():
                    if k in fields:
                        v = super(fileHandler, self)._encrypt_non_ssn_ccn(v, conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])
                    tmp[k] = v
                output.append(tmp)
            
            return output
        
    def removefile(self, filepath, filename):
        os.remove(os.path.join(filepath, filename))

