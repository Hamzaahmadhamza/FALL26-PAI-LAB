from flask import Flask, render_template, request
from embeddings import search

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_response():
    user_input = request.args.get("msg")
    results = search(user_input)

    response = ""
    for q, a in results:
        response += f"Q: {q}\nA: {a}\n\n"

    return response

if __name__ == "__main__":
    app.run(debug=True)