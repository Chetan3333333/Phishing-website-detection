from flask import Flask, render_template, request
import pickle
import re
from urllib.parse import urlparse

app = Flask(__name__)

# Load model
with open("models/phishing_model.pkl", "rb") as f:
    model = pickle.load(f)


def extract_features(url):
    features = []

    features.append(len(url))
    features.append(1 if "https" in url else 0)
    features.append(url.count("."))
    features.append(url.count("-"))
    features.append(url.count("@"))
    features.append(sum(c.isdigit() for c in url))

    ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    features.append(1 if re.search(ip_pattern, url) else 0)

    domain = urlparse(url).netloc
    features.append(domain.count("."))

    return features


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    url = request.form["url"]

    features = extract_features(url)
    prediction = model.predict([features])[0]

    # 1 = Legitimate, 0 = Phishing
    if prediction == 0:
        result = "⚠️ Phishing Website"
    else:
        result = "✅ Legitimate Website"

    return render_template("index.html", prediction_text=result)


if __name__ == "__main__":
    app.run(debug=True)