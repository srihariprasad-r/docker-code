import sys
from vaultClass import hvacClient
from fileHandler import fileHandler
from dbc import DBClient
import argparse
import configparser

customer_table = '''
CREATE TABLE IF NOT EXISTS customers (
    cust_no SERIAL PRIMARY KEY,
    birth_date varchar(255) NOT NULL,
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    create_date varchar(255) NOT NULL,
    social_security_number varchar(255) NOT NULL,
    credit_card_number varchar(255) NOT NULL,
    address varchar(255) NOT NULL,
    salary varchar(255) NOT NULL
)
'''

seed_customers = '''
INSERT into customers (birth_date, first_name, last_name, create_date, social_security_number, credit_card_number, address, salary)
     VALUES
  ('2023-03-10', 'Larry', 'Johnson', '2020-01-01T14:49:12.301977', '360-56-6750', '3600-5600-6750-0000', 'Tyler, Texas', '7000000')
'''

class Demo(fileHandler, DBClient, hvacClient):
    def __init__(self, url='', token='', namespace='', **params):
        hvacClient.__init__(self,url, token, namespace)
        if params:
            if 'filetype' in params:
                fileHandler.__init__(self,**params)
            if 'host' in params:
                DBClient.__init__(self, url, token, namespace,**params)
        self.client = self.get_vault_client()
        self.customer_table = customer_table
        self.seed_customers = seed_customers
        self.customer_schema = ['birth_date', 'first_name', 'last_name', 'create_date', 'social_security_number', 'credit_card_number', 'address', 'salary']

    @staticmethod
    def get_config_entries():
        conf = configparser.ConfigParser()
        with open('config.ini') as f:
            conf.read_file(f)
        return conf
    
    @classmethod
    def constructorFactory(cls, params):
        return cls(**params)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str, required=True)
    parser.add_argument('--apply', type=str)

    if 'file' in sys.argv:
        parser.add_argument('--filetype', type=str, required=True)
        parser.add_argument('--filepath', type=str, required=True)
        parser.add_argument('--csvdelimiter', type=str)

    args = parser.parse_args()
    # load config
    conf = Demo.get_config_entries()
    # file encryption
    if args.type == 'file':
        params = {
            'filetype': args.filetype,
            'filepath': args.filepath,
            'csvdelimiter': args.csvdelimiter if args.csvdelimiter else ','
        }

        dbc = Demo(url=conf['VAULT']['Address'], token=conf['VAULT']['Token'], namespace=conf['VAULT']['Namespace'], **params)
        if not args.apply:
            # prepare csv file for encryption
            if args.filetype == 'csv':
                dbc.prepare_file(dbc.filename, entries=dbc.csventries)
            if args.filetype == 'json':
                dbc.prepare_file(dbc.filename)
            if args.filetype == 'parquet':
                dbc.prepare_file(dbc.filename, entries=dbc.csventries)
            if args.filetype == 'avro':
                dbc.prepare_file(dbc.filename, entries=dbc.csventries)
        if args.apply and args.apply == 'encrypt':
            flag = True
            # encrypt values
            encryptedlist = dbc.encryptfiles(conf)
            # rewrite encrypted fields to new file
            if args.filetype == 'csv':
                dbc.prepare_file(dbc.targetencryptfilename, entries=encryptedlist)
            if args.filetype == 'json':
                dbc.prepare_file(dbc.targetencryptfilename, entries=encryptedlist, flag = flag)
            if args.filetype == 'parquet':
                dbc.prepare_file(dbc.targetencryptfilename, df=encryptedlist)
                # removes csv which was prepared first
                dbc.removefile(dbc.file_path, dbc.csvfile)
            if args.filetype == 'avro':
                dbc.prepare_file(dbc.targetencryptfilename, df=encryptedlist)
                # removes csv which was prepared first
                dbc.removefile(dbc.file_path, dbc.csvfile)
            # remove old file
            dbc.removefile(dbc.file_path, dbc.filename)
    # table encryption
    if args.type == 'table':
        params = {
            'host': conf['DATABASE']['ADDRESS'], 
            'dbname': conf['DATABASE']['Database'],
            'table': conf['DATABASE']['TABLE']
        }
        dbc = Demo(url=conf['VAULT']['Address'], token=conf['VAULT']['Token'], namespace=conf['VAULT']['Namespace'], **params)
        conn = dbc.pgsql_connection(client = dbc.client)
        if not args.apply:
            dbc.executeSQL(customer_table, conn)
            dbc.executeSQL(seed_customers, conn)
        if args.apply and args.apply == 'encrypt':
            rows = dbc.get_table_rows(conf=conf,table='customers', conn=conn)
            for row in rows:
                stmt = dbc.insert_statement(row, conf)
                dbc.executeSQL(stmt, conn)
        if args.apply and args.apply == 'decrypt':
            rows = dbc.get_table_rows(conf=conf, where=' WHERE cust_no=2', table='customers', conn=conn)
            print(rows)
