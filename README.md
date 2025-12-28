# Shopping List
Shopping List is a very simple shared shopping list to use with your family and friends!
It is written in Python and uses the Flask framework. It implements some basic username and password authentication.

This is a hobby project which I built in 2hrs, I needed something with these requirements which is not overly complex.

Disclaimer: I have no idea how safe the authentication is and if there are bugs so don't store sensitive information on it ;-).

## Installation
1. Clone this repo
2. Install the required Python packages via `pip install -r requirements.txt`
3. Make the following files and folders inside the repo: `data (file)`, `instance/db.sqlite (folder and file)`
4. CHANGE THE SECRET KEY IN `config.py`

## Add users
This is limited to just adding users and not removing them, to add a user run `python add-user.py`

## Running the tool
Run `python main.py`
It runs on `0.0.0.0:8080`

## Features
There is:
- no HTTPS
- no automated updates
- no racecondition protection
- no logging
- a nice UI which scales on mobile devices!

## Future features
- Dynamic updating of the shopping list
- Images for products
- User delection
- User updates
