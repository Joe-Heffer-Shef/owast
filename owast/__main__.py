import owast.app_factory

app = owast.app_factory.create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
