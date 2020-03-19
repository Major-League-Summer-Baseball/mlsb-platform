'''
Name: Dallas Fraser
Date: 2014-07-20
Project: MLSB API
Purpose: To create an application to act as an api for the database
'''
from api import app
if __name__ == "__main__":
    start = False
    port = 5000
    while not start and port < 5010:
        try:
            app.run(host='0.0.0.0', debug=True, port=port)
            start = True
        except OSError as e:
            print(e)
            print(f"Port:{port} taken trying another")
            port += 1
