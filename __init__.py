from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY']="secretkey123"

@app.route("/home")
def home():
 return "<h1>Hello world v10 </h1>"

if __name__ == "__main__":
   app.run()
