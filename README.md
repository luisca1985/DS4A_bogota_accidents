# Bogotá Accidents
## Prerequisites
- [Install Git](https://git-scm.com/downloads)
- [Install python 3](https://www.python.org/downloads/)
- [Install Docker](https://docs.docker.com/engine/install/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

## Configurarion
### Start the Project

Clone the project.
odio esto!
```git
git clone git@github.com:luisca1985/DS4A_bogota_accidents.git
```

Access to the folder.

```bash
cd DS4A_bogota_accidents
```

### Create environment variables

Create an `.env` file with:

```
VAR="value of the variable"
```


### Docker
#### Run the application

```
docker-compose up --build
```

Build the images and run the containers in the background.

```
docker-compose up --build -d
```

#### Display logs

Displays log output from services and follows it.

```
docker-compose logs -f
```

#### Attach to the application

Attach to the containers.

```
docker-compose up --attach-dependencies
```

##### Stop application

If it is necessary stop the servies:
- Attach to the containers (see above)
- Press `CRTL + C`

#### Conect with prompt

Get an interactive prompt for the application

```
docker-compose exec app bash
```

### Virtual Environment
#### Linux and Mac
Create virtual environment

```bash
python3 -m venv .venv
```

Activate virtual environment

```bash
source .venv/bin/activate
```

Deactivate virtual environment

```bash
deactivate
```
#### Windows

```
pip install virtualenv
```
```
virtualenv .venv
```
```
.venv/Scripts/activate
```
Should you have any problem, execute:
```
Set-ExecutionPolicy Unrestricted -Scope Process
```

#### Install packages

```bash
pip install -r requirements.txt
```

## Run the Application

Go to the navigator and text

```http
http://0.0.0.0:8050/
```

![alt text](readmepics/graph_test.png)