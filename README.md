# DevOps Apprenticeship: Project Exercise

## Getting started

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from a bash shell terminal:

---------------------
### On macOS and Linux
```bash
$ source setup.sh
```
### On Windows (Using Git Bash)
```bash
$ source setup.sh --windows
```


Once the setup script has completed and all packages have been installed, start the Flask app by running:
```bash
$ flask run
```
--------------------

### With Vagrant - output goes to log.txt
```bash
$ vagrant provision
$ vagrant up
```

------------


You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

### Dev setup
.env should contain the following environment variables:
- TRELLO_BOARD_ID: string
- TRELLO_API_KEY: string
- TRELLO_SERVER_TOKEN: string 

The Trello board must contain lists of "Todo" "In progress" and "Done"

Please install geckodriver and place it on your PATH for selenium tests to work: https://github.com/mozilla/geckodriver/releases


-------
Run with Gunicorn and docker:
Place .env file somewhere

run 
```bash
docker build --tag todo-app:latest && docker run -p 5000:5000/tcp -d --env-file ..\.env todo-app:latest
```
where "..\.env" is the path to your environment variables

