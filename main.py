from flask import Flask, render_template, request
app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('index.html')

@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       first_name = request.form.get("name")
       return "Your name is "+first_name 
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)