# Libgen Telegram Bot

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Libgen Telegram Bot can be used to fetch books from ```https://libgen.is``` using Telegram. It searches the Libgen database and shows the first 10 search result with a inline menu to choose from to download. See screenshot for more

## Installation

 #### 1. On Local System

```sh
$ git clone https://github.com/1337w0rm/Libgen-Telegram-Bot.git
$ cd Libgen-Telegram-Bot
$ pip install -r requirements.txt
```
- Open ```common.py``` file in any text editor.
- Change ```mode``` variable to "dev" from "prod" and put your Bot token in ```TELEGRAM_ACCESS_TOKEN``` variable.

- Run
    ```
    python main.py
    ```

#### 2. On Install Heroku
    
- Clone this repository on your local system
    ```
    git clone https://github.com/1337w0rm/Libgen-Telegram-Bot.git
    ```
 - Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
 - Login to your account with the below command

     ```
    heroku login
    ```
 - Create a new heroku app:
     ```
     heroku create appname
    ```
- Go to Libgen-Telegram-Bot directory on your local system
    ```
    cd Libgen-Telegram-Bot
    ```
- Select This App in your Heroku-cli
    ```
    heroku git:remote -a appname
    ```
- Open ```common.py``` and add your Bot Token to ```TELEGRAM_ACCESS_TOKEN``` and Heroku app name to ```HEROKU_APP_NAME``` variables.

- Add Private Credentials and Config Stuff:
    ```
    git add . 
    ```
- Commit new changes:
    ```
    git commit -m "First Push"
    ```
- Push Code to Heroku:
    ```
    git push heroku master
    ```
- Enable Heroku Dyno
    ```
    heroku ps:scale web=1
    ```