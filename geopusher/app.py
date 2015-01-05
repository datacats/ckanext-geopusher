import ckanapi

from flask import Flask
app = Flask(__name__)

@app.route('/')
def process_webhook():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
