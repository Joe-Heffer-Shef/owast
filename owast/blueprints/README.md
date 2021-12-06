These are the modules of the application. See: [Modular Applications with Blueprints](https://flask.palletsprojects.com/en/2.0.x/blueprints/).

Each of these must be registered when the Flask app is created. This is done automatically so each module here must include a file called "views.py" that contains an object called `blueprint`.