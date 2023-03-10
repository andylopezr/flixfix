<h1 align="center">
  <br>
  <img src="https://i.imgur.com/3jOQG7W.jpeg" alt="flixfix" width="200">
  <br>
</h1>
<h4 align="center">Your fix for personal movie records.</h4>

<p align="center">
  <img src="https://i.imgur.com/XLdzAme.gif" width="800" />
</p>

## Key Features

* Registration - with email and password
    - Validate if email is valid
    - Validate if email is registered
    - Complete password validation

* Login features
    - Validate email and passwor matches

* Add your favorite movies
    - Make them public or private

* Secure Authentication features

* JSON requests and responses

## How to use

> The project is deployed on [AWS](http://ec2-54-91-233-8.compute-1.amazonaws.com/api/docs) you'll find all the endpoints that are available with documentation, please try them on!

* <a href="http://ec2-54-91-233-8.compute-1.amazonaws.com/api/docs">Click here to access the API endpoints</a>

> Movie creation example:

```bash
POST
{
  "title": "Pirates of the Caribbean",
  "score": 8.8,
  "description": "A movie about pirates",
  "review": "amazing",
  "is_private": true
}

RESPONSE
201
{
  "title": "Pirates of the Caribbean"
}
```

## Built with

* Python 3.10.6
* Django 4.1.5
* Django Ninja 0.20.0
* gunicorn 20.1.0
* nginx 1.18.0
* sqlite3

## Requirements

* [X] Create a registration service that receives an email and a password.
    * [X] Validate email is a valid email address.
    * [X] Validate email is not already registered in the database.
    * [X] Validate password contains at least 10 characters, one lowercase letter, one uppercase letter and one of the following characters: !, @, #, ? or ].
    * [X] If any of the above is not valid, send back a meaningful response.


* [X] Allow login into the server with an email and a password.
    * [X] Validate email is a valid email address
    * [X] Validate email is already registered in the database
    * [X] Validate email and password matches for a previous registered user.
    * [X] If any of the above is not valid send back a meaningful response.
    * [X] If all of the above are valid send back a payload including some way for users to identify themselves for subsequent requests. That way to identify users should be invalid after 20 minutes and the user must login again to continue communication with the server.


* [X] Allow logged in users to do CRUD operations into a table/collection of the topic you picked above.
    * [X] Users should be able to create a new element that can only be retrieved by themselves (Private item), or that can be retrieved by others (Public item).
    * [X] Users should be able to read all public elements in the table/collection.
    * [X] Users should be able to read all elements created by themselves.
    * [X] Users should be able to edit at least one field in one of their private items.
    * [X] Validate that users are trying to read or update their own private elements, otherwise send a meaningful response.
