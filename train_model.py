import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("newdataset.csv")

# Keep only URL and label
data = data[["URL", "label"]]

# -----------------------
# Feature Extraction
# -----------------------
import re
from urllib.parse import urlparse

def extract_features(url):
    features = []

    # URL length
    features.append(len(url))

    # HTTPS
    features.append(1 if "https" in url else 0)

    # Count dots
    features.append(url.count("."))

    # Count hyphen
    features.append(url.count("-"))

    # Count @
    features.append(url.count("@"))

    # Count digits
    features.append(sum(c.isdigit() for c in url))

    # IP address check
    ip_pattern = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    features.append(1 if re.search(ip_pattern, url) else 0)

    # Subdomains
    domain = urlparse(url).netloc
    features.append(domain.count("."))

    return features


# Extract features
X = data["URL"].apply(extract_features)
X = pd.DataFrame(X.tolist())

y = data["label"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# Create models folder if not exists
if not os.path.exists("models"):
    os.makedirs("models")

# Save model
with open("models/phishing_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved successfully!")