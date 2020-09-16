Ansible uses command to run by default, "-a" represents argument to that module.
Use "-m" to use module instead
```console
ansible -i inventory multi -a "hostname"

ansible -i inventory multi -m "ping"

ansible -i inventory multi -a "df -h"

ansible -i inventory multi -a "free -h"
```
Ansible creates forks to run the arguments in parallel, to make it as sequential, run with below

-f represents number of forks on servers, by default it is 5
```console
ansible -i inventory multi -a "hostname" -f 1
```
Ansible will use '-b' which takes sudo access to install packages, here we will use yum module and install ntp server
-b and --become are synonymus
```console
ansible -i inventory multi -b -m yum -a "name=ntp state=present"
```
--ask-become-pass will request for sudo passwork, -k does the same
```console
ansible -i inventory multi --become --ask-become-pass -m yum -a "name=ntp state=present"
```
enabled=yes will cause restart of the service deamons upon reboot
```console
ansible -i inventory multi -b -m service -a "name=ntpd state=started enabled=yes"
```
-B represents timelimit in seconds until which ansible will work for the task to be done, -p 0 refers to exit
```console
ansible -i inventory multi -b -B 3600 -p 0 -a "yum -y install"
```
Above command will provide job id, which can be passed to async_status module
```console
ansible -i inventory multi -b -m async_status -a "jid=........"
```
Ansible vault will be used to store api_keys/secrets etc, below command will encrypt
```console
ansible-vault encrypt playbook.yml
```
To execute playbook which has secrets, there is --ask-vault-pass argument to be passed
```console
ansible-playbook playbook.yml --ask-vault-pass
````
Ansible vault playbooks can be edited without decrypting the encrypted version
```console
ansible-vault edit playbook.yml
```
And vault passwords can be changed using
```console
$ ansible-vault rekey playbook.yml
```