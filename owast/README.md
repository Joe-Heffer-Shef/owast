# Ingress web app

This is an application to provide browser-based user interface for secure, robust multi-file upload and metadata input for experiments.

The entry point for the application is a [https://flask.palletsprojects.com/en/2.0.x/](https://flask.palletsprojects.com/en/2.0.x/) which is defined in `owast.app_factory.create_app()`. This is served using Web Server Gateway Interface (WSGI) implemented using [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/).

# Azure App Service

This container is designed to emulate the Azure App Service environment. See: [Quickstart: Create a Python app using Azure App Service on Linux](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=bash&pivots=python-framework-flask). This uses uWSGI to serve Python apps using either Flask or Django web frameworks.

There are certain parameters that this hosted environment uses, which can also be customised. Here we use the default options where possible. See: [Configure a Linux Python app for Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/configure-language-python). Azure will start the app using `requirements.txt` to install Python package dependencies and use `startup.txt` to tell it how to run the WSGI interface. See [Flask start-up commands](https://docs.microsoft.com/en-us/azure/developer/python/tutorial-deploy-app-service-on-linux-04) for customising the app start-up process.
