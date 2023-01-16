# FLIX FIX
<img src= "https://i.imgur.com/3jOQG7W.jpeg">

> your fix for personal movie records.


## Backend API

## Requirements:

* [ ] Create a registration service that receives an email and a password.
    * [ ] Validate email is a valid email address.
    * [ ] Validate email is not already registered in the database.
    * [ ] Validate password contains at least 10 characters, one lowercase letter, one uppercase letter and one of the following characters: !, @, #, ? or ].
    * [ ] If any of the above is not valid, send back a meaningful response.


* [ ] Allow login into the server with an email and a password.
    * [ ] Validate email is a valid email address
    * [ ] Validate email is already registered in the database
    * [ ] Validate password contains at least 10 characters, one lowercase letter, one uppercase letter and one of the following characters: !, @, #, ? or ].
    * [ ] Validate email and password matches for a previous registered user.
    * [ ] If any of the above is not valid send back a meaningful response.
    * [ ] If all of the above are valid send back a payload including some way for users to identify themselves for subsequent requests. That way to identify users should be invalid after 20 minutes and the user must login again to continue communication with the server.


* [ ] Allow logged in users to do CRUD operations into a table/collection of the topic you picked above.
    * [ ] Users should be able to create a new element that can only be retrieved by themselves (Private item), or that can be retrieved by others (Public item).
    * [ ] Users should be able to read all public elements in the table/collection.
    * [ ] Users should be able to read all elements created by themselves.
    * [ ] Users should be able to edit at least one field in one of their private items.
    * [ ] Validate that users are trying to read or update their own private elements, otherwise send a meaningful response.
