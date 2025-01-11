
from flask import Flask, request, jsonify
import joblib
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("path/to/your/firebase/credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load the trained model
model = joblib.load("linear_regression_model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        groceries = data["groceries"]
        entertainment = data["entertainment"]
        utilities = data["utilities"]
        actual_savings = data["actual_savings"]
        
        # Prepare data for prediction
        input_data = np.array([[groceries, entertainment, utilities]])
        predicted_savings = model.predict(input_data)[0]
        
        # Generate suggestion based on comparison
        if actual_savings < predicted_savings:
            suggestion = "You need to save more!"
        elif actual_savings > predicted_savings:
            suggestion = "Great job saving more than predicted!"
        else:
            suggestion = "You are saving as predicted!"
        
        # Save data to Firestore
        user_data = {
            "groceries": groceries,
            "entertainment": entertainment,
            "utilities": utilities,
            "predicted_savings": predicted_savings,
            "actual_savings": actual_savings,
            "suggestion": suggestion
        }
        db.collection("user_data").add(user_data)
        
        # Return the result to the user
        return jsonify({
            "predicted_savings": predicted_savings,
            "suggestion": suggestion
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
