from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# initialize sqlite!!


# Load the trained model
model = joblib.load("linear_regression_model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        print("Received data:", data)

        # replace and create 1 table and 4 rows using grocery, entertainment, utilities, and actual_savings
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
        
        # replace Save data to sqlite
        user_data = {
            "groceries": groceries,
            "entertainment": entertainment,
            "utilities": utilities,
            "predicted_savings": predicted_savings,
            "actual_savings": actual_savings,
            "suggestion": suggestion
        }

        print("hello from the other side")

        print("adssadasd")
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
