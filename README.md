<h1>Simple Number API</h1>

A simple api that takes a number and returns interesting mathematical properties about it, along with a fun fact.

<h2>Dependencies</h2>
blinker==1.9.0
certifi==2025.1.31
charset-normalizer==3.4.1
click==8.1.8
Flask==3.1.0
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.5
MarkupSafe==3.0.2
requests==2.32.3
urllib3==2.3.0
Werkzeug==3.1.3


<h2>Steps</h2>

create an azure virtual instance using azure cli (Feel free to use your own cloud platform service):
```
az vm create --name myVm --resource-group hng --size Standard_D2s_v3 --image Ubuntu24.04 --nsg-rule SSH --admin-username <your_username> --admin-password <your_password>
```
open port 80:

```
az network nsg rule create --resource-group hng --nsg-name myVmNSG --name Allow-HTTP --protocol tcp --priority 1001 --destination-port-ranges 80 --access Allow --direction Inbound
```
set up the ssh keys for your connection

```
az vm create \
   --resource-group hng \
   --name myVm \
   --image Ubuntu2204\
   --admin-username <azureuser> \
   --ssh-key-value ~/.ssh/id_rsa.pub
```
copy the private ssh key to your .ssh folder and change file permissions:

```
chmod 400 <your private key>.pem
```

ssh into the server. Answer the prompts as needed:

```
ssh -i ~/.ssh/<your-private-key> <username>@<vm-public-ip>
```

<h4>After creating a folder on the vm, clone the above repository:</h4>

```
git clone https://github.com/Benson-Gikonyo/simple-number-api
```

<h4>install the dependencies:</h4>

```
pip install -r requirements.txt.
```
<h4>Start the server:</h4>

type the following command into the terminal to run the server:

```
python3 number.py
```

<h4>Test the api with a number of your choice</h4>
