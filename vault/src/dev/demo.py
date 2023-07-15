import sys
from app import hvacClient
from fileHandler import fileHandler
from dbc import DBClient
import argparse
import configparser

class Demo(fileHandler, DBClient, hvacClient):
    def __init__(self, url='', token='', namespace='', **params):
        hvacClient.__init__(self,url, token, namespace)
        if params:
            if 'filetype' in params:
                fileHandler.__init__(self,**params)
            if 'host' in params:
                DBClient.__init__(self, **params)
        self.client = self.get_vault_client()

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
            dbc.prepare_file(dbc.filename, dbc.csventries)
        if args.apply and args.apply == 'encrypt':
            # encrypt values
            csvencryptedlist = dbc.encryptfiles()
            # rewrite encrypted fields to new file
            dbc.prepare_file(dbc.targetencryptfilename, csvencryptedlist)
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
        # prepare csv file for encryption
        conn = dbc.pgsql_connection(client = dbc.client)
        if not args.apply:
            dbc.executeSQL(dbc.customer_table, conn)
            dbc.executeSQL(dbc.seed_customers, conn)
        if args.apply and args.apply == 'encrypt':
            rows = dbc.get_table_rows(table='customers')
            for row in rows:
                stmt = dbc.insert_statement(row, conf)
                dbc.executeSQL(stmt, conn)
        if args.apply and args.apply == 'decrypt':
            rows = dbc.get_table_rows(conf=conf, where=' WHERE cust_no=2', table='customers')
            print(rows)
