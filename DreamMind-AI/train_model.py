import os
import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsRestClassifier

print(" Training started...")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "dream_expressions_dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")

os.makedirs(MODEL_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.strip().str.lower()

print(" Columns:", list(df.columns))

if "dream_text" not in df.columns or "emotions" not in df.columns:
    raise Exception("Missing required columns")

df = df.dropna(subset=["dream_text", "emotions"])

def clean_labels(x):
    x = str(x).lower().replace(";", ",")
    labels = [i.strip() for i in x.split(",") if i.strip()]
    return labels if len(labels) > 0 else ["relief"]  

df["emotions"] = df["emotions"].apply(clean_labels)

df = df[df["emotions"].apply(len) > 0]

X = df["dream_text"].fillna("")
y = df["emotions"]

mlb = MultiLabelBinarizer()
y_encoded = mlb.fit_transform(y)

print(" Classes learned:", list(mlb.classes_))

model = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1,2),
        stop_words="english",
        max_features=8000
    )),
    ("clf", OneVsRestClassifier(
        LogisticRegression(
            max_iter=3000,
            class_weight="balanced"
        )
    ))
])

model.fit(X, y_encoded)

joblib.dump(model, os.path.join(MODEL_DIR, "pipeline.joblib"))
joblib.dump(mlb, os.path.join(MODEL_DIR, "mlb.joblib"))

print(" Model trained successfully!")