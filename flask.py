

from flask import Flask, request, jsonify, render_template
import joblib
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("path_to_your_firebase_key.json")  # Add your Firebase service key
firebase_admin.initialize_app(cred)
db = firestore.client()

# Flask App
app = Flask(__name__)

# Load Trained Model
model = joblib.load("linear_regression_model.pkl")

# Homepage Route
@app.route("/")
def index():
    return render_template("index.html")

# Predict Savings
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    groceries = data.get("groceries", 0)
    entertainment = data.get("entertainment", 0)
    utilities = data.get("utilities", 0)

    # Input for Model
    user_input = [[groceries, entertainment, utilities]]
    prediction = model.predict(user_input)

    # Save Prediction to Firebase
    user_id = data.get("user_id", "default_user")  # User ID can be dynamic
    db.collection("users").document(user_id).set({
        "groceries": groceries,
        "entertainment": entertainment,
        "utilities": utilities,
        "predicted_savings": prediction[0]
    }, merge=True)

    return jsonify({"predicted_savings": prediction[0]})

# Leaderboard
@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    users_ref = db.collection("users")
    docs = users_ref.stream()
    leaderboard_data = [
        {"user": doc.id, **doc.to_dict()} for doc in docs
    ]
    # Sort by savings (highest first)
    leaderboard_data.sort(key=lambda x: x["predicted_savings"], reverse=True)
    return jsonify(leaderboard_data)

if __name__ == "__main__":
    app.run(debug=True)
