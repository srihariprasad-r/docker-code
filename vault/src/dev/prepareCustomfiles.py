import csv
import os
import json
import pandas as pd
import fastparquet
import avro.io
from collections import namedtuple
from fastavro import parse_schema, writer
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

class preparefiles(object):
  def __init__(self,filepath='', file_type='csv', delimit=','):
    self.file_path = filepath
    self.file_type = file_type
    self.delimit = delimit if self.file_type == 'csv' else None
    self.csventries = [['Sno', 'birth_date', 'first_name', 'last_name',
              'created_date', 'ssn', 'credit_card_number', 'address', 'salary'],
              ['1', '2023-03-10', 'Ash Ketchum','Jr.', '2020-01-01T14:49:12.301977',
              '360-56-6750', '3600-5600-6750-0000', 'NY, NY',  '352200'],
              ['2', '2023-03-11',  'Lui Ken', 'Se', '2023-01-01T14:49:12.301977',
              '887-56-6786', '1823-4296-7852-0010','NY, NY', '80000'],
              ['3', '2023-03-12', 'Chang', 'Lee',  '2020-03-01T14:49:12.301977',
              '788-78-5670','7782-7787-7780-0011',  'NY, NY', '100000'],
              ['4', '2023-03-14', 'Xu',  'Yong', '2020-01-03T14:49:12.301977',
                '360-48-4198', '3600-5600-7889-1011',  'NY, NY',  '7788550'],
              [ '5',  '2023-03-15',  'Roberts',  'Henry','2021-01-01T14:49:12.301977',
                '122-66-7895',  '7330-8896-4799-1000',  'NY, NY',  '63300'],
              [ '6',  '2023-03-15',  'Keo',  'Lamn',  '2020-08-07T14:49:12.301977',
                '785-80-8860',  '8778-5600-6750-7892',  'NY, NY',  '78522'],
              ['7',  '2023-03-17', 'Sam', 'Eric', '2020-11-01T14:49:12.301977',
                '363-45-8755',  '5546-7752-7885-4296',  'NY, NY',  '455000'],
              [ '8',  '2023-03-18', 'Paul',  'Misor',  '2008-01-01T14:49:12.301977',
                '378-96-8777',  '9985-6630-8852-8432', 'NY, NY',  '100000'],
              [ '9', '2023-03-19', 'Richard',  'David',  '2014-01-01T14:49:12.301977',
                '870-06-6650', '7799-6630-6750-9732',  'NY, NY', '875200']
              ]
    self.jsonschema = self.csventries[0]
    self.jsonentries = self.csventries[1:]  
    self.avroschema = """
      {
        "namespace": "data_avro.avro",
        "type": "record",
        "name": "data_avro",
        "fields": [
            {"name": "Sno", "type": "string"},
            {"name": "birth_date", "type": "string"},
            {"name": "first_name", "type": "string"},
            {"name": "last_name", "type": "string"},
            {"name": "created_date", "type": "string"},
            {"name": "ssn", "type": "string"},
            {"name": "credit_card_number", "type": "string"},
            {"name": "address", "type": "string"},
            {"name": "salary", "type": "string"}
          ]
      }
      """

  def prepare_csv_file(self, filename, csventries):
    if not os.path.exists(self.file_path):
       os.makedirs(self.file_path)
    with open(os.path.join(self.file_path , filename), 'w', newline='') as file:
        writer = csv.writer(file, delimiter=self.delimit if self.delimit else ',')
        # writer.writeheader()
        writer.writerows(csventries)

  def prepare_json_file(self, filename, schema='', entries=''):
    if not os.path.exists(self.file_path):
       os.makedirs(self.file_path)
    if entries and schema:
      output = []
      for val in entries:
        tmp = {}
        for i in range(len(val)):
          tmp[schema[i]] = val[i]
        output.append(tmp)
    with open(os.path.join(self.file_path , filename), 'w', newline='') as file:
      json.dump(output if schema and entries else entries, file)

  def prepare_parquet_file(self, filename, df=''):
    if not os.path.exists(self.file_path):
       os.makedirs(self.file_path)
    if len(df) == 0:
      pd.read_csv(os.path.join(self.file_path, filename)).to_parquet(os.path.join(self.file_path, 'data.parquet'))
      csv_df = pd.read_parquet(os.path.join(self.file_path, 'data.parquet'))
      print('******* sample contents from parquet file *******')
      print(csv_df.head())
      print('******* *******')
    if len(df) > 0:
      filename = 'encrypted_data.parquet'
      df.to_parquet(os.path.join(self.file_path, filename))
      print('******* sample contents from encrypted parquet file *******')
      p_df = pd.read_parquet(os.path.join(self.file_path, filename))
      for row in p_df:
        print(p_df[row])
      print('******* *******')

  def prepare_avro_file(self, filename, df=''):
    if not os.path.exists(self.file_path):
       os.makedirs(self.file_path)
    if len(df) == 0:
      fields = ('Sno', 'birth_date', 'first_name', 'last_name', 'created_date', 'ssn', 'credit_card_number', 'address', 'salary')
      schemaRecord = namedtuple('schemaRecord', fields)
      parsed_schema = parse_schema(json.loads(self.avroschema))

      lst = []

      with open(os.path.join(self.file_path, filename), 'r') as file:
        file.readline()
        reader = csv.reader(file, delimiter=self.delimit if self.delimit else ',')
        for records in map(schemaRecord._make, reader):
          record = dict((f, getattr(records, f)) for f in records._fields)
          lst.append(record)

      with open(os.path.join(self.file_path, 'data.avro'), "wb") as fp:
        writer(fp, json.loads(self.avroschema), lst)
    
    if df:
      with open(os.path.join(self.file_path, 'encrypted_data.avro'), 'wb') as wp:
        writer(wp, json.loads(self.avroschema), df)
      # print('******* sample contents from encrypted avro file *******')
      # p_df = DataFileReader(open("enrypted_data.avro", "rb"), DatumReader())
      # for row in p_df:
      #   print(row)
      # print('******* *******')
      for row in df:
        print(row)
