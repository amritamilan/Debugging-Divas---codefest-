import pandas as pd

#training data set
train_data = {
    "Groceries": [300, 400, 200, 100, 500, 600, 700, 300],
    "Entertainment": [200, 300, 150, 50, 400, 350, 500, 250],
    "Utilities": [150, 200, 100, 50, 300, 250, 150, 180],
    "Savings": [50, 100, 200, 300, 0, 150, 100, 250]
}
#putting data in rows and tables 
df = pd.DataFrame(train_data)
x = df[["Groceries", "Entertainment", "Utilities"]]
y = df["Savings"]
print(x)
print(y)



#training linear regression model
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split



x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

print("Training Features (X_train):")
print(x_train)
print("\nTesting Features (X_test):")
print(x_test)
print("Training Features (y_train):")
print(y_train)
print("\nTesting Features (y_test):")
print(y_test)


model = LinearRegression()

try:
    model.fit(x_train, y_train)
    accuracy = model.score(x_test, y_test)
    print(f"\nThe accuracy of the model is {accuracy:.2f}")
except Exception as e:
    print(f"Error during training: {e}")

print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

#saving model for future use
import joblib
joblib.dump(model, "linear_regression_model.pkl")
print("model saved!")

loaded_model = joblib.load("linear_regression_model.pkl")
print("Model loaded!")

# sliders
import streamlit as st

# Load the saved model
# model = joblib.load("linear_regression_model.pkl")

# Streamlit sliders for user input
groceries = st.slider("Groceries Spending ($)", 0, 1000, 200)
entertainment = st.slider("Entertainment Spending ($)", 0, 1000, 150)
utilities = st.slider("Utilities Spending ($)", 0, 1000, 100)


# Combine inputs into a single array
user_data = [[groceries, entertainment, utilities]]

# Predict savings
predicted_savings = model.predict(user_data)[0]
st.write(f"Predicted Savings: ${predicted_savings:.2f}")
print("predicted")