import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# Load the pickled model (ensure model.pkl is in the same directory)
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    print("Error: 'model.pkl' not found. Please ensure the model.pkl exists in the same directory as your application code.")
    exit(1)

@app.route('/')
def home():
    """
    Renders the home page (index.html).
    """
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predicts sales and renders results on the index.html page. Handles potential errors gracefully.
    """

    if request.method == 'POST':
        try:
            # Extract features from the form (assuming numerical input)
            try:
                int_features = [float(x) for x in request.form.values()]  # Handle potential conversion errors
            except ValueError:
                return render_template('index.html', prediction_text="Invalid input. Please enter numerical values.")

            final_features = [np.array(int_features)]

            # Make prediction using the loaded model
            prediction = model.predict(final_features)[0]
            output = round(prediction, 2)

            return render_template('index.html', prediction_text='Amount of total sales: $ {}'.format(output))
        except Exception as e:
            print(f"Error during prediction: {e}")
            return render_template('index.html', prediction_text="An unexpected error occurred. Please try again later.")

if __name__ == '__main__':
