<h1 align="center">
  <br>
  <img src="https://i.imgur.com/3jOQG7W.jpeg" alt="flixfix" width="200">
  <br>
</h1>
<h4 align="center">Your fix for personal movie records.</h4>

![screenshot](https://im5.ezgif.com/tmp/ezgif-5-28c9a625a9.gif)


### Backend API

### Requirements:

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
