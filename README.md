# flask-gunicorn-auth

This is a very basic Flask application which can be used as a starter template for building your Flask RESTful API applications.

## Features
 - Gunicorn server setup
 - URL to register your users at <your-host>/api/v1/users
 - JWT authentication at <your-host>/api/v1/login
 - Mongo DB as database
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
cp scripts/myproject.sh /etc/init.d/
chmod +x /etc/init.d/myproject.sh
systemctl daemon-reload
service myproject start
iptables -I INPUT -p tcp -m state --state NEW -m tcp --dport 5000 -j ACCEPT
```

## Routes
 - Create a user: POST /api/v1/users
 - Login with this user: POST /api/v1/login
 - Create a resoure: POST /api/v1/filestems
 - Fetch all resoures: GET /api/v1/filestems
 - Fetch a resoure: GET /api/v1/filestems/<fs_id>
 - Delete a resoure: DELETE /api/v1/filestems/<fs_id>
 - Modify a resoure: PUT /api/v1/filestems/<fs_id>

## Usage

#### Create a new user
```sh
curl -X POST http://127.0.0.1:5000/api/v1/users -d '{"username": "your_username", "email": "your_email", "password": "your_password"}' -H 'Content-Type: application/json'
{
  "message": "The user has been created",
  "data": {
    "_id": "62e1a9a05bf5b9aea7f307ca",
    "username": "your_username",
    "email": "your_email",
    "password": "pbkdf2:sha256:260000$EYkPpOxkfLUqYAfS$645331d29491967b955150421e3aeb89105fe9015eb1344d0f2c92fb0ae6e038",
    "active": true
  }
}
```


#### Login with this user
```sh
curl -X POST http://127.0.0.1:5000/api/v1/login -d '{"username": "your_username",  "password": "your_password"}' -H 'Content-Type: application/json'
{
  "message": "Successfully fetched auth token",
  "data": {
    "_id": "62e1a6d95bf5b9aea7f307c9",
    "username": "your_username",
    "email": "your_email",
    "active": true,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI2MmUxYTZkOTViZjViOWFlYTdmMzA3YzkiLCJleHAiOjE2NTkwNDI1Mjl9.U1VjT6d-L1ITz4B0Wp-BRpOUY_KSYaIndfg1a6vO7s8"
  }
}
```


#### Create a resource
```sh
curl -X POST http://127.0.0.1:5000/api/v1/filesystems -d '{"filesystem" : "fs1", "size": 1024, "media": "ssd"}' -H 'Content-Type: application/json' --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFua3VyIn0.JESn3tcL7_-zmTwHdqkyHtdcOUeDKCw_gd4-DwfOPIg"
{
  "message": "Successfully created a new filesystem",
  "data": {
    "_id": "62e1a9f45bf5b9aea7f307cb",
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
      "_id": "62e1a9f45bf5b9aea7f307cb",
      "filesystem": "fs1",
      "size": 1024,
      "media": "ssd"
    }
  ]
}
```

#### Get a specific resource
```sh
curl -X GET  http://127.0.0.1:5000/api/v1/filesystems/62e1a9f45bf5b9aea7f307cb -H 'Content-Type: application/json' --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFua3VyIn0.JESn3tcL7_-zmTwHdqkyHtdcOUeDKCw_gd4-DwfOPIg"
{
  "message": "Successfully fetched filesystems details",
  "data": {
      "_id": "62e1a9f45bf5b9aea7f307cb",
      "filesystem": "fs1",
      "size": 1024,
      "media": "ssd"
    }
}
```

#### Update a specific resource
```sh
curl -X PUT  http://127.0.0.1:5000/api/v1/filesystems/62e1a9f45bf5b9aea7f307cb -d '{"size":1024000, "media": "HDD"}' -H 'Content-Type: application/json' --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFua3VyIn0.JESn3tcL7_-zmTwHdqkyHtdcOUeDKCw_gd4-DwfOPIg"
{
  "message": "The filesystem has been updated",
  "data": {
    "_id": "62e1a9f45bf5b9aea7f307cb",
    "name": "fs1",
    "size": 1024000,
    "media": "HDD"
  }
}
```

#### Delete a specific resource
```sh
curl -X DELETE  http://127.0.0.1:5000/api/v1/filesystems/62e1a9f45bf5b9aea7f307cb -H 'Content-Type: application/json' --header "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFua3VyIn0.JESn3tcL7_-zmTwHdqkyHtdcOUeDKCw_gd4-DwfOPIg"
{
  "message": "The filesystem has been deleted",
  "data": null
}

```
