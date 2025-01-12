from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Load the trained model
model = joblib.load("linear_regression_model.pkl")


# Helper function to initialize SQLite database and table
def init_db():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()

    # Drop and recreate the table
    cursor.execute("DROP TABLE IF EXISTS User_Data")
    cursor.execute("""
        CREATE TABLE User_Data (
            groceries FLOAT,
            entertainment FLOAT,
            utilities FLOAT,
            actual_savings FLOAT,
            predicted_saving FLOAT,
            suggestion VARCHAR(255)
        )
    """)
    conn.commit()
    conn.close()


# Call to initialize the database at the start
init_db()


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Parse incoming JSON data
        data = request.json
        print("Received data:", data)

        # Extract data from JSON request
        groceries = float(data["groceries"])
        entertainment = float(data["entertainment"])
        utilities = float(data["utilities"])
        actual_savings = float(data["actual_savings"])

        # Prepare data for prediction
        input_data = np.array([[groceries, entertainment, utilities]])
        predicted_savings = model.predict(input_data)[0]

        # Generate suggestion based on the comparison
        if actual_savings < predicted_savings:
            suggestion = "You need to save more!"
        elif actual_savings > predicted_savings:
            suggestion = "Great job saving more than predicted!"
        else:
            suggestion = "You are saving as predicted!"

        # Insert the data into SQLite
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        insert_query = f"""
            INSERT INTO User_Data (
                groceries, entertainment, utilities, actual_savings, predicted_saving, suggestion
            ) VALUES ({groceries}, {entertainment}, {utilities}, {actual_savings}, {predicted_savings}, {suggestion})
        """
        cursor.execute(insert_query)
        conn.commit()
        conn.close()

        # Return the response
        return jsonify({
            "predicted_savings": predicted_savings,
            "suggestion": suggestion
        })

    except Exception as e:
        print("Error occurred:", e)
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
