from appconfig import create_app

if __name__ == "__main__":
    myapp = create_app()
    myapp.run(debug=True)