import hvac
import psycopg2
import base64
import os
import argparse

hvac_client = {'url': os.environ['VAULT_ADDR']}

client = hvac.Client(**hvac_client)
psql_host = os.environ['PSQL_ADDR']
db_name = "postgres"

def encyrpt(plain_text, encrypt_key):
    encoded = base64.b64encode(plain_text.encode('utf-8'))
    cipher = client.secrets.transit.encrypt_data(name=encrypt_key,
                                                 plain_text=str(encoded, 'utf-8')
                                                 )
    return cipher['data']['ciphertext']

def decrypt(ciphertext, decrypt_key):
    decrypt_data = client.secrets.transit.decrypt_data(name=decrypt_key,
                                                 ciphertext=ciphertext
                                                 )
    return str(base64.b64decode(decrypt_data['data']['plaintext']), 'utf-8')

def pgsql_connection(role):
    psql_credentials = client.secrets.database.generate_credentials(name=role)
    conn = psycopg2.connect(host=psql_host, database=db_name, \
                            user=psql_credentials['data']['uername'],
                            password=psql_credentials['data']['password'])
    return conn

def execute(sqlstmt, username, cipher, connection):
    cursor = connection.cursor()
    cursor.execute(sqlstmt, {username, cipher})
    connection.commit()

def retrieve(sqlstmt, username, connection):
    cursor = connection.cursor()
    cursor.execute(sqlstmt,{username})
    records = cursor.fetchall()
    return records

def main():
    assert client.is_authenticated()
    parser = argparse.ArgumentParser()
    parser.add_argument("--decrypt", "-d",help="decrypts password")
    parser.add_argument("--encrypt", "-e", help="encrypts password")
    parser.add_argument("--key", help="specify key for encryption")

    args = parser.parse_args()

    if args.encrypt:
        print("password: ", end="")
        password = input()