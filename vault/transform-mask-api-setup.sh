export VAULT_ADDR=http://localhost:8200
export VAULT_TOKEN=root
export VAULT_NAMESPACE=dev

# create namespace dev
vault namespace delete dev/
vault namespace create dev

#enable the transform secret engine for masking
vault secrets disable data_protection/masking/transform
vault secrets enable  -path=data_protection/masking/transform transform

#Define a role ccn with transformation ccn
vault write data_protection/masking/transform/role/ccn transformations=ccn

#create a transformation of type masking using a template defined in next step and assign role ccn to it that we created earlier
vault write data_protection/masking/transform/transformation/ccn \
        type=masking \
        template="card-mask" \
        masking_character="#" \
        allowed_roles=ccn
#create the template for masking
vault write data_protection/masking/transform/template/card-mask type=regex \
        pattern="(\d{4})-(\d{4})-(\d{4})-\d{4}" \
        alphabet="builtin/numeric"
#test if the masking transformation was created successfully
vault list data_protection/masking/transform/transformation
vault read  data_protection/masking/transform/transformation/ccn