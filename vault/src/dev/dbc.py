import psycopg2
from hvac import hvacClient

class DBClient(hvacClient):
    def __init__(self, host, dbname, table):
        self.host = host
        self.dbname = dbname
        self.table = table
        self.client = hvacClient.get_vault_client()

    def pgsql_connection(self, role=''):
        psql_credentials = self.client.read('data_protection/database/creds/vault-demo-app')
        conn = psycopg2.connect(host=self.host, database=self.dbname,
                                user=psql_credentials['data']['username'],
                                password=psql_credentials['data']['password'])
        return conn
    
    def executeSQL(self, sqlstmt, cursor):
        try:
            cursor.execute(sqlstmt)
        except:
            raise Exception('sql statement throws error. Aborting!')
    
    def get_table_rows(self, table, limit=1):
        sql = " SELECT * FROM " + self.dbname + '.' + str(table) + ' LIMIT {}'.format(limit)
        cursor = self.pgsql_connection.cursor()
        self.executeSQL(sql, cursor)
        results = []

        for row in cursor:
            r = {}
            r['customer_number'] = row[0]
            r['birth_date'] = row[1]
            r['first_name'] = row[2]
            r['last_name'] = row[3]
            r['create_date'] = row[4]
            r['ssn'] = row[5]
            r['ccn'] = row[6]
            r['address'] = row[7]
            r['salary'] = row[8]
            if self.client is not None:
                r['birth_date'] = hvacClient._decrypt_non_ssn_ccn(r['birth_date'])
                r['ssn'] = hvacClient._decode_ssn_ccn(r['ssn'])
                r['ccn'] = hvacClient._decode_ssn_ccn(r['ccn'])
                r['address'] = hvacClient._decrypt_non_ssn_ccn(r['address'])
                r['salary'] = hvacClient._decrypt_non_ssn_ccn(r['salary'])
            results.append(r)
        
        return results
