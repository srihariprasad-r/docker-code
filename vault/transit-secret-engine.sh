#!/bin/sh

# Example:
export VAULT_ADDR=http://localhost:8200
export VAULT_TOKEN=root
export VAULT_TOKEN=root

echo "Enabling the vault transit secrets engine..."

# Enable the transit secret engine
vault secrets disable data_protection/transit
vault secrets enable -path=data_protection/transit transit

# Create our customer key
vault write  -f data_protection/transit/keys/customer-key

vault write data_protection/transit/encrypt/customer-key plaintext=$(base64 << "my secret data")