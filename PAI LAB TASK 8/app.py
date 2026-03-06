from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Route to get random joke
@app.route("/joke")
def get_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        if response.status_code == 200:
            joke_data = response.json()
            return jsonify({
                "setup": joke_data.get("setup"),
                "punchline": joke_data.get("punchline")
            })
        else:
            return jsonify({"error": "Failed to fetch joke"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)