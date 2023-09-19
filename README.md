[![wakatime](https://wakatime.com/badge/github/Brad123ghost/UrbanCo.svg)](https://wakatime.com/badge/github/Brad123ghost/UrbanCo)
---


# UrbanCo
This Microservices prototype is being developed for a demonstration for INFS 605 Microservices. It features two selected microservices which are the Catalogue and Account.

#### Frontend Service
Shows the website view, calling either the catalogue or account service depending on the action performed

#### Catalogue Service
Sends back the current products to display on the website

#### Account Service
Handles user login and signup data and processes.

# How to Run
Download docker and docker-compose, alternatively, download docker desktop.

### CD into the folder
Open CMD or Terminal and CD into the main folder
``` cd (path)/urbanco```

### Build each image
Then CD into each of the microservice folders from the ```Urbanco``` folder and build the docker image
#### Account Service
```
  cd account-service
  docker build -t accountservice:latest .
```
#### Catalogue Service
```
  cd catalogue-service
  docker build -t catalogueservice:latest .
```
#### Frontend Service
```
  cd frontend-service
  docker build -t frontendservice:latest .
```
### Deploy the containers
From the Urbanco folder
Run the following command: 
```Docker compose -f deploy.yaml up -d```

After running the compose command, wait 12-20 seconds before trying to access HTTP://localhost, as the database containers will take some time to load fully. 

To remove the compose: 
```Docker compose -f deploy.yaml down```

# Accessing the Databases
Once all the containers are running and 12-20 seconds have passed for the DB initialization, visit HTTP://localhost:9090

Make sure to select **PostgreSQL** for the image
#### Catalogue Database
Server: ```cataloguedbservice``` <br>
Username: ```urbanco```<br>
Password: ```admin```<br>
Database: ```cataloguedb```

#### Account Database
Server: ```accountdbservice```<br>
Username: ```urbanco```<br>
Password: ```admin```<br>
Database: ```accountdb```

# Demo Accounts
Two demo accounts have been set up: Admin and Customer. These accounts are set up to test the functionality of the admin dashboard which can be accessed via HTTP://localhost/dashboard if you are logged into the admin account.
#### Admin Account
Email: ```admin@urbanco.com```
Password: ```password```
#### Customer Account
Email: ```customer1@gmail.com```
Password: ```password```
