from appconfig import create_app

if __name__ in ['__main__', 'appconfig.main']:
    app = create_app()
    #app.run(host='0.0.0.0', debug=True, port=5000)