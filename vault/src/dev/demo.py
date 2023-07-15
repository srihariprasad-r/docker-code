import sys
from app import hvacClient
from fileHandler import fileHandler
import argparse
import configparser

class Demo(fileHandler, hvacClient):
    def __init__(self, url='', token='', namespace='', **params):
        hvacClient.__init__(self,url, token, namespace)
        fileHandler.__init__(self,**params)
        self.client = self.get_vault_client()

    @staticmethod
    def get_config_entries():
        conf = configparser.ConfigParser()
        with open('config.ini') as f:
            conf.read_file(f)
        return conf
    

if __name__ == '__main__':
    conf = Demo.get_config_entries()
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', type=str, required=True)
    parser.add_argument('--apply', type=str)

    if 'file' in sys.argv:
        parser.add_argument('--filetype', type=str, required=True)
        parser.add_argument('--filepath', type=str, required=True)
        parser.add_argument('--csvdelimiter', type=str)

    args = parser.parse_args()
    if args.type == 'file':
        params = {
            'filetype': args.filetype,
            'filepath': args.filepath,
            'csvdelimiter': args.csvdelimiter if args.csvdelimiter else ','
        }

        dbc = Demo(url=conf['VAULT']['Address'], token=conf['VAULT']['Token'], namespace=conf['VAULT']['Namespace'], **params)
        # prepare csv file for encryption
        dbc.prepare_file(dbc.filename, dbc.csventries)
        # encrypt values
        csvencryptedlist = dbc.encryptfiles()
        # rewrite encrypted fields to new file
        dbc.prepare_file(dbc.targetencryptfilename, csvencryptedlist)

