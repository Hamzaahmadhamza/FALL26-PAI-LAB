from flask import Flask, render_template, request, jsonify
import joblib
import os
import numpy as np

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "pipeline.joblib")
MLB_PATH = os.path.join(BASE_DIR, "model", "mlb.joblib")

pipeline = joblib.load(MODEL_PATH)
mlb = joblib.load(MLB_PATH)


def get_meaning(emotions):

    if not emotions:
        return "This dream shows mixed subconscious signals."

    if "fear" in emotions:
        return "You are dealing with anxiety or hidden fear."
    if "sadness" in emotions:
        return "You may be emotionally low."
    if "relief" in emotions:
        return "You are recovering from stress."
    if "joy" in emotions:
        return "Positive emotional energy is present."

    return "Your dream reflects inner emotional processing."


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json.get("text", "").strip()

        if not data:
            return jsonify({
                "result": [],
                "meaning": "Please enter dream text",
                "top_predictions": []
            })
  
        pred = pipeline.predict([data])

        emotions = []
        try:
            emotions = list(mlb.inverse_transform(pred)[0])
        except:
            emotions = ["unknown"]

        top_predictions = []

        try:
            prob = pipeline.predict_proba([data])[0]
            top_idx = np.argsort(prob)[::-1][:3]

            top_predictions = [
                {
                    "emotion": mlb.classes_[i],
                    "score": round(float(prob[i]), 3)
                }
                for i in top_idx
            ]
        except:
            top_predictions = [
                {"emotion": "unknown", "score": 1.0}
            ]

        return jsonify({
            "result": emotions,
            "meaning": get_meaning(emotions),
            "top_predictions": top_predictions
        })

    except Exception as e:
        return jsonify({
            "result": [],
            "meaning": "Server error",
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)