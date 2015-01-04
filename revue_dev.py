from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'VTK-revue development! Is working'

if __name__ == '__main__':
    app.run()
