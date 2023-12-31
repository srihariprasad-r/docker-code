import csv
import os
import json
import pandas as pd
# import fastparquet
import avro.io
from collections import namedtuple
from fastavro import parse_schema, writer, reader
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
              '360-56-6750', '3600-5600-6750-0000', 'NY',  '352200'],
              ['2', '2023-03-11',  'Lui Ken', 'Se', '2023-01-01T14:49:12.301977',
              '887-56-6786', '1823-4296-7852-0010','NY', '80000'],
              ['3', '2023-03-12', 'Chang', 'Lee',  '2020-03-01T14:49:12.301977',
              '788-78-5670','7782-7787-7780-0011',  'NY', '100000'],
              ['4', '2023-03-14', 'Xu',  'Yong', '2020-01-03T14:49:12.301977',
                '360-48-4198', '3600-5600-7889-1011',  'NY',  '7788550'],
              [ '5',  '2023-03-15',  'Roberts',  'Henry','2021-01-01T14:49:12.301977',
                '122-66-7895',  '7330-8896-4799-1000',  'NY',  '63300'],
              [ '6',  '2023-03-15',  'Keo',  'Lamn',  '2020-08-07T14:49:12.301977',
                '785-80-8860',  '8778-5600-6750-7892',  'NY',  '78522'],
              ['7',  '2023-03-17', 'Sam', 'Eric', '2020-11-01T14:49:12.301977',
                '363-45-8755',  '5546-7752-7885-4296',  'NY',  '455000'],
              [ '8',  '2023-03-18', 'Paul',  'Misor',  '2008-01-01T14:49:12.301977',
                '378-96-8777',  '9985-6630-8852-8432', 'NY',  '100000'],
              [ '9', '2023-03-19', 'Richard',  'David',  '2014-01-01T14:49:12.301977',
                '870-06-6650', '7799-6630-6750-9732',  'NY', '875200']
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

  def config_fields(self, file, filename):
    with open(file, 'r') as f:
      file_contents = f.read()

    entries = json.loads(file_contents)
    encrypted_fields_list = dict()

    for k, v in entries.items():
      for i in range(len(v)):
        if v[i]['source_file_name'] == filename:
          for m, n in v[i]['fields'].items():
            encrypted_fields_list[m] = n

    return encrypted_fields_list
    
  def read_csv_file_to_html(self,filename, delimiter=','):
      with open(os.path.join(self.filepath, filename), 'r', newline='') as f:
        content = f.readlines()
      fields = self.config_fields(os.path.join(os.path.dirname(__file__), 'files_config.json'),filename)
      #reading file content into list
      # content = [line for line in content]
      # fields = ['birth_date', 'ssn', 'credit_card_number', 'address', 'salary']
      rows = [x for x in content]
      PIIindex = [idx for idx, x in enumerate(self.jsonschema) if x in fields]
      table = """<table align="left" border="1" cellpadding="3" cellspacing="3">\n<thead>\n"""
      table += "".join(["<th>"+cell+"</th>" for cell in self.jsonschema])
      table += "</thead>\n"
      table += "<tbody>\n"
      #Converting csv to html row by row
      for row in rows[1:]:
        line = row.split(',')
        table+= "<tr>\n"
        i = 0
        for col in line:
          if i in PIIindex and filename.find('encrypted') == -1:
            table +=  "    <td class='blurclass'>{0}</td>\n".format(col.strip())
          else:
            table +=  "   <td>{0}</td>\n".format(col.strip())
          i += 1
        table+= "</tr>\n"
        # table+= "<tr>" + "".join(["<td>" + cell if cell.find(',') == -1 else '-'.join(cell.split(',')) + "</td>\n" for cell in row.split(',')]) + "</tr>" + "\n"
      table += "</tbody>\n"
      table+="</table><br>"
      return table

  def read_parquet_file_to_html(self,filename):
      cols = ['Sno', 'birth_date', 'first_name', 'last_name','created_date', 'ssn', 'credit_card_number', 'address', 'salary']
      df = pd.read_parquet(path=os.path.join(self.file_path, filename), columns=cols)
      fields = self.config_fields(os.path.join(os.path.dirname(__file__), 'files_config.json'), filename)
      pd.set_option('colheader_justify', 'center')
      dict_data = [df.to_dict(), df.to_dict('index')]

      return_str = """<table align="left" border="1" cellpadding="3" cellspacing="3">\n<thead>\n"""
      return_str += "".join(["<th>"+cell+"</th>" for cell in self.jsonschema])
      return_str += "</thead>\n"
      return_str += "<tbody>\n"

      for key in dict_data[1].keys():
        return_str = return_str + '<tr>' + str(key)
        for subkey in dict_data[1][key]:
          if subkey in fields and filename.find('encrypted') == -1:
            return_str = return_str + "<td class='blurclass'>" + str(dict_data[1][key][subkey]) + '</td>\n'
          else:
            return_str = return_str + '<td>' + str(dict_data[1][key][subkey]) + '</td>\n'
        return_str = return_str + '</tr>\n'
      return_str += "</tbody>\n"
      return_str += "</table><br>"

      # html_string = '''
      #   <body>
      #     {table}
      #   </body>
      # '''
      # return html_string.format(table=df.to_html(classes='pandas'))
      return return_str
  
  def read_avro_file_to_html(self,filename):
    avro_records = []
    with open(os.path.join(self.file_path, filename), 'rb') as fo:
      avro_reader = reader(fo)
      for record in avro_reader:
        avro_records.append(record)

    df_avro = pd.DataFrame(avro_records)

    pd.set_option('colheader_justify', 'center')
    fields = self.config_fields(os.path.join(os.path.dirname(__file__), 'files_config.json'), filename)
    dict_data = [df_avro.to_dict(), df_avro.to_dict('index')]

    return_str = """<table align="left" border="1" cellpadding="3" cellspacing="3">\n<thead>\n"""
    return_str += "".join(["<th>"+cell+"</th>" for cell in self.jsonschema])
    return_str += "</thead>\n"
    return_str += "<tbody>\n"

    for key in dict_data[1].keys():
      return_str = return_str + '<tr>' + str(key)
      for subkey in dict_data[1][key]:
        if subkey in fields and filename.find('encrypted') == -1:
          return_str = return_str + "<td class='blurclass'>" + str(dict_data[1][key][subkey]) + '</td>\n'
        else:
          return_str = return_str + '<td>' + str(dict_data[1][key][subkey]) + '</td>\n'
      return_str = return_str + '</tr>\n'
    return_str += "</tbody>\n"
    return_str += "</table><br>"

    # html_string = '''
    #     <body>
    #       {table}
    #     </body>
    # '''
    # return html_string.format(table=df_avro.to_html(classes='pandas'))
    return return_str

  def prepare_csv_file(self, filename, csventries):
    if not os.path.exists(self.file_path):
       os.makedirs(self.file_path)
    with open(os.path.join(self.file_path , filename), 'w', newline='') as file:
        writer = csv.writer(file, delimiter=self.delimit if self.delimit else ',')
        # writer.writeheader()
        writer.writerows(csventries)
    return self.read_csv_file_to_html(filename,delimiter=self.delimit if self.delimit else ',')

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
    
    return json.dumps(output if schema and entries else entries)

  def prepare_parquet_file(self, filename, df=''):
    if not os.path.exists(self.file_path):
       os.makedirs(self.file_path)
    if len(df) == 0:
      pd.read_csv(os.path.join(self.file_path, filename)).to_parquet(os.path.join(self.file_path, 'data.parquet'))
      csv_df = pd.read_parquet(os.path.join(self.file_path, 'data.parquet'))
      print('******* sample contents from parquet file *******')
      print(csv_df.head())
      print('******* *******')
      return self.read_parquet_file_to_html('data.parquet')
    if len(df) > 0:
      filename = 'encrypted_data.parquet'
      df.to_parquet(os.path.join(self.file_path, filename))
      print('******* sample contents from encrypted parquet file *******')
      p_df = pd.read_parquet(os.path.join(self.file_path, filename))
      for row in p_df:
        print(p_df[row])
      print('******* *******')
      return self.read_parquet_file_to_html(filename)

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
      
      return self.read_avro_file_to_html('data.avro')
    
    if df:
      with open(os.path.join(self.file_path, 'encrypted_data.avro'), 'wb') as wp:
        writer(wp, json.loads(self.avroschema), df)
      print('******* sample contents from encrypted avro file *******')
      p_df = DataFileReader(open(os.path.join(self.file_path,"encrypted_data.avro"), "rb"), DatumReader())
      for row in p_df:
        print(row)
      print('******* *******')
      return self.read_avro_file_to_html('encrypted_data.avro')
