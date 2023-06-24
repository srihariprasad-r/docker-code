import hvac 
import base64
import requests

class hvacClient(object):
    def __init__(self, hvac_url, token, namespace, ssn_role='', ccn_role=''):
        self.hvac_url = hvac_url
        self.token = token
        self.namespace = namespace
        self.ssn_role = ssn_role
        self.ccn_role = ccn_role

    def get_vault_client(self):
        hvac_client = {}
        hvac_client['url'] = self.hvac_url
        hvac_client['token'] = self.token
        hvac_client['namespace'] = self.namespace
        return hvac.Client(**hvac_client)
    
    def encrypt_non_ssn_ccn(self, keyname, mountpath, value):
        response = self.vault_client.secrets.transit.encrypt_data(
            mount_point=mountpath,
            name=keyname,
            plaintext=base64.b64encode(value.encode()).decode('ascii')
            )
        
        return response['data']['ciphertext']

    def decrypt_non_ssn_ccn(self, keyname, mountpath, value):
        response = self.vault_client.secrets.transit.decrypt_data(
            mount_point=mountpath,
            name=keyname,
            ciphertext=value
        )

        plaintext = response['data']['plaintext']
        return base64.b64decode(plaintext).decode()
    
    def encode_ssn_ccn(self, ssn, transform_mount_point, value):
        url = self.vault_client.url + "/v1/" + transform_mount_point + "/encode/" + self.ssn_role if ssn else self.ccn_role
        payload = "{\n  \"value\": \"" + value + "\",\n  \"transformation\": \"" + self.ssn_role if ssn else self.ccn_role + "\"\n}"
        headers = {
            'X-Vault-Token': self.vault_client.token,
            'X-Vault-Namespace': self.namespace,
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        return response.json()['data']['encoded_value']

    def decode_ssn_ccn(self, ssn, transform_mount_point, value):
        url = self.vault_client.url + "/v1/" + transform_mount_point + "/decode/" + self.ssn_role if ssn else self.ccn_role
        payload = "{\n  \"value\": \"" + value + "\",\n  \"transformation\": \"" + self.ssn_role  if ssn else self.ccn_role + "\"\n}"
        headers = {
            'X-Vault-Token': self.vault_client.token,
            'X-Vault-Namespace': self.namespace,
            'Content-Type': "application/json",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        return response.json()['data']['decoded_value']

    def _encrypt_non_ssn_ccn(self, value):
        keyname = self.conf['VAULT']['KeyName']
        mountpath = self.conf['VAULT']['secretPath']
        return self.encrypt_non_ssn_ccn(keyname, mountpath, value)
