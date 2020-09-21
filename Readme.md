# Simple Cocktail database
Just a help to remember cocktail recipes 


## Installation
1. Create venv `py -m venv`
2. Install requirements.txt `pip install -r requirements.txt`
3.Upgrade/ Create database file:   
Start venv, go in wg_app dircetory and run `flask db upgrade` 

## Requirements
- python Version 3.8.5
- git


## Next steps:
- User Management (Administration)
- Export and Import Recipes as csv (for safety)
  - not via cli,   via UI
- Change Ingredients and a longer description 
- Further changes to change from Cocktails to general Recipes
- Write Tests

## Tests
Run tests, with activated venv:
`py tests.py`

### Test server for testing error mails:

- in extra cmd with venv on:   
  `py -m smtpd -n -c DebuggingServer localhost:8025`
- extra cmd with venv on:
`set FLASK_DEBUG=0  `
`set MAIL_SERVER=localhost  `
`set MAIL_PORT=8025`

## .env FIle
For setting environment variables   
````
# Creaet a uuid
SECRET_KEY= UUID

# Set Mail Serever, here a gmail account
MAIL_SERVER=smtp.googlemail.com   //  localhost  
MAIL_PORT=587   // 8025  
MAIL_USE_TLS=1  
MAIL_USERNAME=  
MAIL_PASSWORD=  

# The number of cocktails on one side
POSTS_PER_PAGE=10

# if not sqlite, set for db server, here postgres
DATABASE_URL=postgresql+psycopg2://{user}:{pw}@{url}/{db}
````

## Deployment on Linux server:

#### Requirements  
- Linux Server with following packages
    - git: to get the project
    - supervisor: to run the project in the background and restarting after booting
- A Web server: f.e. gunicorn or uwsgi
- A database server if required: f.e. mysql-server or postgres
`sudo apt-get -y install mysql-server postfix supervisor nginx git`

#### Installation:
- get the project: `https://github.com/sheuschk/wg_app.git`
- create a venv and start it
- install requirements
- install the Webserver `pip install gunicorn`
- install database drivers if necessary
- create a .env File
- Save the app as env var in the profile 
`echo "export FLASK_APP=microblog.py" >> ~/.profile`
- Create db: `flask db upgrade`

#### Starting:
Running the application with supervisor. It restarts automatically after booting or if it crashes
The Username ubuntu is your username 
- `sudo nano /etc/supervisor/conf.d/wg_app.conf`  
[program:wg_app]  
command=/home/ubuntu/wg_app/venv/bin/gunicorn -b localhost:8000 -w 4 wg_app:app  
directory=/home/ubuntu/wg_app  
user=ubuntu  
autostart=true  
autorestart=true  
stopasgroup=true  
killasgroup=true  
- `sudo supervisorctl reload`

#### nginx
Make the application accessible for other devices
- Create a certificat. For tests or development this can be a self signed certificat
- `mkdir certs`
- `openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
  -keyout certs/key.pem -out certs/cert.pem`
- `sudo rm /etc/nginx/sites-enabled/default`
- write following file for configurations. In etc/nginx/sites-enabled/wg_app:
```` 
server {
    # listen on port 80 (http)
    listen 80;
    server_name _;
    location / {
        # redirect any requests to the same URL but on https
        return 301 https://$host$request_uri;
    }
}
server {
    # listen on port 443 (https)
    listen 443 ssl;
    server_name _;

    # location of the self-signed SSL certificate
    ssl_certificate /home/ubuntu/wg_app/certs/cert.pem;
    ssl_certificate_key /home/ubuntu/wg_app/certs/key.pem;

    # write access and error logs to /var/log
    access_log /var/log/wg_app_access.log;
    error_log /var/log/wg_app_error.log;

    location / {
        # forward application requests to the gunicorn server
        proxy_pass http://localhost:8000;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        # handle static files directly, without forwarding to the application
        alias /home/ubuntu/wg_app/app/static;
        expires 30d;
    }
}
````
- `sudo service nginx reload`

#### Updating:
````
$ git pull                              # download the new version
$ sudo supervisorctl stop wg_app        # stop the current server
$ flask db upgrade                      # upgrade the database
$ sudo supervisorctl start wg_app       # start a new server
````

#### Safety
- Install ufw (Uncomplicated firewall) and open just for ssh, http and https
````angular2html
$ sudo apt-get install -y ufw
$ sudo ufw allow ssh
$ sudo ufw allow http
$ sudo ufw allow 443/tcp
$ sudo ufw --force enable
$ sudo ufw status
````

- in /etc/ssh/sshd_config: PermitRootLogin: no
