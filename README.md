# flask-gunicorn-auth

This is a very basic Flask application which can be used as a starter template for building your Flask RESTful API applications.

## Features
 - Gunicorn server setup
 - URL to register your users at <your-host>/api/v1/usres
 - JWT authentication at <your-host>/api/v1/login
 - Provisioned route file for all your routes with blueprints

## Built With
This App was developed with the following stack:
 - Python
 - Flask
 - Flask-restful
 - Gunicorn Web Server
  
## Requirements
 - Python 3.6+
 - Python pip

## Installation

```sh
cd /home
git clone https://github.com/AnkurMathur14/flask-gunicorn-auth.git
cd flask-gunicorn-auth
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cp apiserver.sh /etc/init.d/
chmod +x /etc/init.d/apiserver.sh
systemctl daemon-reload
service apiserver start
iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 5000 -j ACCEPT
```

## Routes
 - Create a user: POST /api/v1/users
 - Login with this user: POST /api/v1/login
 - Create a resoure: POST /api/v1/filestems
 - Fetch a resoure: GET /api/v1/filestems/<filestems_name>
 - Delete a resoure: DELETE /api/v1/filestems/<filestems_name>
 - Modify a resoure: PUT /api/v1/filestems/<filestems_name>

## Usage

#### Create a new user
```sh
curl -X POST http://127.0.0.1:5000/api/v1/users -d '{"username": "your_username", "email": "your_email", "password": "your_password"}'
{
  "message": "Successfully created new user",
  "data": {
    "username": "your_username",
    "email": "your_email",
    "password": "your_password"
  }
}
```


#### Login with this user
```sh
curl -X POST http://127.0.0.1:5000/api/v1/login -d '{"username": "your_username",  "password": "your_password"}'
{
  "message": "Successfully fetched auth token",
  "data": {
    "username": "your_username",
    "email": "your_email",
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFua3VyIn0.JESn3tcL7_-zmTwHdqkyHtdcOUeDKCw_gd4-DwfOPIg"
  }
}
```


#### Create a resource
```sh
curl -X POST http://127.0.0.1:5000/api/v1/filesystems -d '{"filesystem" : "fs1", "size": 1024, "media": "ssd"}' -H 'Content-Type: application/json' --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFua3VyIn0.JESn3tcL7_-zmTwHdqkyHtdcOUeDKCw_gd4-DwfOPIg"
{
  "message": "Successfully created a new filesystem",
  "data": {
    "filesystem": "fs1",
    "size": 1024,
    "media": "ssd"
  }
}
```

#### Get the resource
```sh
curl -X GET  http://127.0.0.1:5000/api/v1/filesystems -H 'Content-Type: application/json' --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFua3VyIn0.JESn3tcL7_-zmTwHdqkyHtdcOUeDKCw_gd4-DwfOPIg"
{
  "message": "Successfully fetched filesystems details",
  "data": [
    {
      "filesystem": "fs1",
      "size": 1024,
      "media": "ssd"
    }
  ]
}
```

