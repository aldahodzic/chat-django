A simple CRUD messaging application to explore the django framework. Allows the creation of users, and the ability for those users to send messages. Uses django's authentication system to authenticate users.

## Endpoints:

### /authenticate
- **GET:**
	- Check to see if the user is already authenticated. Uses cookies to identify user.
- **POST:**
	- Try to login with the user. Post request data contains ['username', 'password']
	
### /authenticate/{id}
- **DELETE:**
	- Logout user with the specified id.


### /messages
- **GET:**
	- Get all messages.
- **POST:**
	- Create new message. Post request data contains ['sender', 'body']. 'sender' is the id of the user that you wish to send the message to.

### /messages/{id}
- **GET:**
	- Get the message with the specified id.
- **PUT:**
	- Update the read status of the message with the specified id. Put request data contains ['is\_read'] 
- **DELETE:**
	- Delete the message with the specified id.

### /users
- **GET:**
	- Get all users.	
- **POST:**
	- Create a new user. Post request data contains ['username', 'password', 
### /users/{id}
- **GET:**
	- Get the user with the specified id.
- **PUT:**
	- Update the user. Put request data may contain ['username', 'password'].
- **DELETE:**
	- Delete the specified user.


### /send/{id}
An html form to send a new message from the user with the specified id.


## Models:
### Message:
	body: The contents of the message.
	time_sent: When the message was sent.
	is_read: Has the message been read?
	sender: The user who sent the message.
	recipient: The user who will receive the message.
### User:
	username: The name the user will be known by.
	password: The password used to authenticate the user
	email: The email used for correspondence to the user.
