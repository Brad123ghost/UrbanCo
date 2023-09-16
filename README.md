# UrbanCo

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

To remove the compose: 
```Docker compose -f deploy.yaml down```
