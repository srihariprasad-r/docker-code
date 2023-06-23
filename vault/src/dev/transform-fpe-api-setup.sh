export VAULT_ADDR=http://localhost:8200
export VAULT_TOKEN=root
export VAULT_NAMESPACE=dev

#enable the transform secret engine
vault secrets disable data_protection/transform
vault secrets enable  -path=data_protection/transform transform

#Define a role ssn with transformation ssn
vault write data_protection/transform/role/ssn transformations=ssn

#create a transformation of type fpe using built in template for social security number and assign role ssn to it that we created earlier
vault write data_protection/transform/transformation/ssn type=fpe template=builtin/socialsecuritynumber tweak_source=internal allowed_roles=ssn
#test if the transformation was created successfully
vault list data_protection/transform/transformation
vault read  data_protection/transform/transformation/ssn