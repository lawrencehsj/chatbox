# About the project
An online chat room that allows user to send and receive messages live to each other, with a few other functions such as user accounts and a friend system. The database contains all these necessary information, in which the web service communicates with the end user and updates accordingly. Additionally, there is an API servie to display the content of messages being exchanged. This project explores the development of webservers using django, authentication and web sockets to accomodate asynchronous requests over the web service. 

User login            |  Chat room
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/58553029/197112327-c947a5b0-0c6a-41c6-a956-41b2c6a22533.png)  |  ![](https://user-images.githubusercontent.com/58553029/197109151-8344c46a-10d7-48a3-8260-33b4348251b0.png)

### Built With
* Django
* Bootstrap
* redis
* postgre sql

### Features
* Account login/creation
* Searching for users
* Chatroom (home)
* Friend list
* API

<br>

## Getting Started
Follow these instructions to get a local copy of this project up and running.

### Prerequisites
* npm
  ```sh
  npm install npm@latest -g
  ```
* django virtual env

### Installation
Initialize the project in the Django environment through a series of commands that automatically creates the set of packages and files required to construct the app:

1. Install NPM packages
   ```sh
   npm install
   ```
2. Workon django virtual environment
3. Install project requirements
   ```sh
   pip install -r requirements.txt
   ```
3. Start the django environment
   ```sh
   django-admin startproject chatbox 
   cd chatbox
   python manage.py startapp account
   python manage.py startapp groupchat
   python manage.py startapp friend
   ```
   
Two terminals are necessary to run the app: One to run redis-server for web sockets, another one for the actual web server. Run each of the following command in separate terminals in the root directory of the project:

1. redis-server
2. python manage.py rumserver 


To run the unit tests:
   ```sh
   cd chatbox
   python manage.py test
   ```
