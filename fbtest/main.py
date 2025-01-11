from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize Firebase
cred = credentials.Certificate("firebase/diva-app-codefest-firebase-adminsdk-5n04t-ede1a02a0f.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load the trained model
model = joblib.load("linear_regression_model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        print("Received data:", data)

        groceries = float(data["groceries"])
        entertainment = float(data["entertainment"])
        utilities = float(data["utilities"])
        actual_savings = float(data["actual_savings"])

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

        print("hello")

        docs = db.collection("user_data")

        print("hello from the other side")

        # for doc in docs.stream():
        #     print("hi")

#         try:
#             # for doc in docs:
#             #     print("hi")
#             #     print(doc)
# #                 print(f"{doc.id} => {doc.to_dict()}")
#         except Exception as e:
#             print(e)

        print("adssadasd")

        # db.collection("user_data").add(user_data)

        # Return the result to the user
        return jsonify({
            "predicted_savings": predicted_savings,
            "suggestion": suggestion
        })

    except Exception as e:
        print("adadad")
        print(e)
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
