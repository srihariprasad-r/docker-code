import psycopg2
from vaultClass import hvacClient
import configparser

class DBClient(hvacClient):
    def __init__(self, **params):
        self.host = params['host']
        self.dbname = params['dbname']
        self.table = params['table']

    @staticmethod
    def get_config_entries():
        conf = configparser.ConfigParser()
        with open('config.ini') as f:
            conf.read_file(f)
        return conf

    def pgsql_connection(self, client, role=''):
        psql_credentials = client.read('data_protection/database/creds/vault-demo-app')
        conn = psycopg2.connect(host=self.host, database=self.dbname,
                                user=psql_credentials['data']['username'],
                                password=psql_credentials['data']['password'])
        return conn
    
    def executeSQL(self, sqlstmt, connection=None):
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(sqlstmt)
            connection.commit()
        except:
            raise Exception('sql statement throws error. Aborting!')
        return cursor
    
    def insert_statement(self, row, conf):
        bdt = super(DBClient,self)._encrypt_non_ssn_ccn(row['birth_date'], conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])
        ssn = super(DBClient,self)._encrypt_non_ssn_ccn(row['social_security_number'], conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])
        ccn = super(DBClient, self)._encrypt_non_ssn_ccn(row['credit_card_number'], conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])
        addr = super(DBClient,self)._encrypt_non_ssn_ccn(row['address'], conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])
        sal = super(DBClient, self)._encrypt_non_ssn_ccn(row['salary'], conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])
        statement = '''INSERT INTO customers (birth_date, first_name, last_name, create_date, \
            social_security_number, credit_card_number, address, salary)
            VALUES  ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');'''\
                    % (str(bdt), \
                       str(row['first_name']), str(row['last_name']), str(row['create_date']), \
                       str(ssn), \
                       str(ccn), \
                       str(addr), \
                       str(sal)
                )
        return statement
    
    def get_table_rows(self, table, conf, where='' , limit=1):
        sql = " SELECT * FROM " +  str(table) + where +  ' LIMIT {}'.format(limit)
        client = super(DBClient, self).get_vault_client()
        connection = self.pgsql_connection(client=client)
        cursor = self.executeSQL(sql, connection)
        results = []

        for row in cursor:
            r = {}

            r['birth_date'] = row[1]
            r['first_name'] = row[2]
            r['last_name'] = row[3]
            r['create_date'] = row[4]
            r['social_security_number'] = row[5]
            r['credit_card_number'] = row[6]
            r['address'] = row[7]
            r['salary'] = row[8]
            if where and self.client:
                r['birth_date'] = super(DBClient,self)._decrypt_non_ssn_ccn(r['birth_date'], conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])
                r['social_security_number'] = super(DBClient, self)._decrypt_non_ssn_ccn(
                    r['social_security_number'], conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])
                r['credit_card_number'] = super(DBClient, self)._decrypt_non_ssn_ccn(
                    r['credit_card_number'], conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])
                r['address'] = super(DBClient, self)._decrypt_non_ssn_ccn(
                    r['address'], conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])
                r['salary'] = super(DBClient, self)._decrypt_non_ssn_ccn(
                    r['salary'], conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])

            results.append(r)

        return results
