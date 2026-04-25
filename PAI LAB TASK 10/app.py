from flask import Flask, render_template, request
import re

app = Flask(__name__)

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    return text

def chatbot(user_input):
    text = preprocess(user_input)

    if any(w in text for w in ["admission","apply","enroll"]):
        return "Admissions are open. You can apply online or visit university office."
    elif any(w in text for w in ["fee","cost","charges"]):
        return "Fee details depend on your program. Check university portal."
    elif any(w in text for w in ["department","courses","program"]):
        return "We offer CS, AI, Electrical and Business departments."
    elif any(w in text for w in ["time","timing","hours"]):
        return "University timing is 8 AM to 4 PM, Monday to Friday."
    elif any(w in text for w in ["location","where","address"]):
        return "University is located at main city campus."
    else:
        return "I can only answer university related questions."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    user_msg = request.args.get("msg")
    return chatbot(user_msg)

if __name__ == "__main__":
    app.run(debug=True)
    