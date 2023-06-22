import hvac
import psycopg2
import base64
import os
import argparse

hvac_client = {'url': 'http://vault-demo:8200',
               'token': 'root', 'namespace': 'dev'}

client = hvac.Client(**hvac_client)
psql_host = os.environ['PSQL_ADDR']
db_name = "postgres"

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


def encyrpt(plain_text, encrypt_key):
    encoded = base64.b64encode(plain_text.encode('utf-8'))
    cipher = client.secrets.transit.encrypt_data(name=encrypt_key,
                                                 plain_text=str(
                                                     encoded, 'utf-8')
                                                 )
    return cipher['data']['ciphertext']


def decrypt(ciphertext, decrypt_key):
    decrypt_data = client.secrets.transit.decrypt_data(name=decrypt_key,
                                                       ciphertext=ciphertext
                                                       )
    return str(base64.b64decode(decrypt_data['data']['plaintext']), 'utf-8')


def pgsql_connection(role=''):
    # psql_credentials = client.secrets.database.generate_credentials(name=role)
    psql_credentials = client.read(
        'data_protection/database/creds/vault-demo-app')
    conn = psycopg2.connect(host='vault_db_1', database=db_name,
                            user=psql_credentials['data']['username'],
                            password=psql_credentials['data']['password'])
    return conn


def execute(sqlstmt, connection):
    cursor = connection.cursor()
    cursor.execute(sqlstmt)
    connection.commit()


def retrieve(sqlstmt, username, connection):
    cursor = connection.cursor()
    cursor.execute(sqlstmt, {username})
    records = cursor.fetchall()
    return records


def main():
    # assert client.is_authenticated()
    parser = argparse.ArgumentParser()
    parser.add_argument("--decrypt", "-d", help="decrypts password")
    parser.add_argument("--encrypt", "-e", help="encrypts password")
    parser.add_argument("--key", help="specify key for encryption")

    args = parser.parse_args()

    pg_conn = pgsql_connection()
    execute(customer_table, pg_conn)
    execute(seed_customers, pg_conn)


main()