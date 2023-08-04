import os, csv
from prepareCustomfiles import preparefiles
from vaultClass import hvacClient
import json
import pandas as pd
# import fastparquet
import avro.io
from avro.datafile import DataFileReader
from avro.io import DatumReader

class fileHandler(preparefiles):
    def __init__(self, hdfs_connection='', aws_connection='', **params):
        self.filepath = params['filepath']
        self.filetype = params['filetype']
        self.delimited = params['csvdelimiter']
        self.filename = 'customers.csv' if self.filetype in ('csv', 'parquet', 'avro') else 'jsoncustomers.json'
        self.targetencryptfilename = None
        self.csvencryptedentries = []
        super(fileHandler, self).__init__(self.filepath, self.filetype, self.delimited)
        
    def prepare_file(self, filename='', entries='', df='', flag=False):
        if self.file_type == 'csv':
            return self.prepare_csv_file(filename=filename, csventries=entries)
        if self.file_type == 'json':
            if not flag:
                return self.prepare_json_file(filename=filename, schema=self.jsonschema, entries=self.jsonentries)
            else:
                return self.prepare_json_file(filename=filename, entries=entries)
        if self.file_type == 'parquet':
            # uses csv as input, so prepare csv before conversion
            self.prepare_csv_file(filename=filename, csventries=entries)
            return self.prepare_parquet_file(filename=filename, df=df)
        if self.file_type == 'avro':
            # uses csv as input, so prepare csv before conversion
            self.prepare_csv_file(filename=filename, csventries=entries)
            return self.prepare_avro_file(filename=filename, df=df)
    
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
        import vaultClass
        fields = self.parse_config_fields(os.path.join('/src/dev', 'fileconfig.json'))
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
        # parquet processing
        if self.file_type == 'parquet':
            self.csvfile = self.filename
            self.filename = 'data.parquet'
            cols = ['Sno', 'birth_date', 'first_name', 'last_name','created_date', 'ssn', 'credit_card_number', 'address', 'salary']
            df = pd.read_parquet(path=os.path.join(self.file_path, self.filename), columns=cols)
            for row in df:
                if row in fields:
                    for i in range(len(df[row])):
                        df[row][i] = super(fileHandler, self)._encrypt_non_ssn_ccn(str(df[row][i]), conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])
            
            return df
        # avro processing
        if self.file_type == 'avro':
            self.csvfile = self.filename
            self.filename = 'data.avro'
            reader = DataFileReader(open(os.path.join(self.file_path, self.filename), 'rb'), DatumReader())
            tmp = []
            for row in reader:
                for a, b in row.items():
                    if a in fields:
                        row[a] = super(fileHandler, self)._encrypt_non_ssn_ccn(str(b), conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])
                tmp.append(row)

            return tmp
        
    def removefile(self, filepath, filename):
        os.remove(os.path.join(filepath, filename))

