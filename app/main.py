from flask import Flask, request, render_template
from script import process_query

app = Flask(__name__)

@app.route("/")
@app.route("/search")
def home():
    return render_template("index.html")

@app.route("/search", methods=['POST'])
def search():
    search_term = request.form['search']
    results = process_query(search_term)
    return render_template("results.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)

