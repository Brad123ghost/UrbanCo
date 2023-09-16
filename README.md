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
#### Account Serivce
```
  cd account-service
  docker build -t accountservice:latest .
```
#### Catalogue Serivce
```
  cd catalogue-service
  docker build -t catalogueserivce:latest .
```
#### Frontend Serivce
```
  cd frontend-serivce
  docker build -t frontendservice:latest .
```

### Deploy the containers
From the Urbanco folder
Run the following command: 
```Docker compose -f deploy.yaml up -d```

After running the compose command, wait 12-20 seconds before trying to access HTTP://localhost as it will take some time for the database containers to fully load 

To remove the compose: 
```Docker compose -f deploy.yaml down```
