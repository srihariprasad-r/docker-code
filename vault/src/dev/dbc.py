import psycopg2
from app import hvacClient
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

class DBClient(hvacClient):
    def __init__(self, host, dbname, url, token, namespace, table=''):
        self.host = host
        self.dbname = dbname
        self.table = table
        self.url = url
        self.token = token
        self.namespace = namespace
        super(DBClient, self).__init__(url, token, namespace)
        self.client = self.get_vault_client()

    @staticmethod
    def get_config_entries():
        conf = configparser.ConfigParser()
        with open('config.ini') as f:
            conf.read_file(f)
        return conf

    def pgsql_connection(self, role=''):
        psql_credentials = self.client.read('data_protection/database/creds/vault-demo-app')
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
    
    def insert_statement(self, row):
        bdt = self._encrypt_non_ssn_ccn(row[1], conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])
        ssn=self._encrypt_non_ssn_ccn(row[5], conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])
        ccn = self._encrypt_non_ssn_ccn(row[6], conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])
        addr=self._encrypt_non_ssn_ccn(row[7], conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])
        sal = self._encrypt_non_ssn_ccn(row[8], conf['VAULT']['KeyName'], conf['VAULT']['secretPath'])
        statement = '''INSERT INTO customers VALUES (birth_date, first_name, last_name, create_date, \
            social_security_number, credit_card_number, address, salary)
            VALUES  ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');'''\
                    % (str(bdt), \
                       str(row[2]), str(row[3]),str(row[4]), \
                       str(ssn), \
                       str(ccn), \
                       str(addr), \
                       str(sal)
                )
        return statement
    
    def get_table_rows(self, table, limit=1):
        sql = " SELECT * FROM " +  str(table) + ' LIMIT {}'.format(limit)
        connection = self.pgsql_connection()
        cursor = self.executeSQL(sql, connection)
        results = []

        for row in cursor:
            results.append(row)
        
        return results
    

if __name__ == '__main__':
    conf = DBClient.get_config_entries()
    dbc = DBClient(host=conf['DATABASE']['ADDRESS'], dbname=conf['DATABASE']['Database'], url=conf['VAULT']['Address'], \
                   token=conf['VAULT']['Token'], namespace=conf['VAULT']['Namespace'])
    conn = dbc.pgsql_connection()
    dbc.executeSQL(customer_table, conn)
    dbc.executeSQL(seed_customers, conn)
    rows = dbc.get_table_rows(table='customers')
    for row in rows:
        stmt = dbc.insert_statement(row)
        dbc.executeSQL(stmt, conn)
