from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello from Our Team Balaji , Hariprasad, Dharanish and Balamurugan </h2>'


if __name__ == "__main__":
    app.run(debug=True)