import pickle
from flask import Flask, request, render_template

app = Flask(__name__)

# Load the pickled model (ensure model.pkl is in the same directory)
with open('model.pkl', 'rb') as f:
  model = pickle.load(f)

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
      try:
        # Convert form values to floats, handle ValueError
        int_features = [float(x) for x in request.form.values()]
      except ValueError:
        return render_template('index.html', prediction_text="Invalid input. Please enter numerical values.")

      final_features = [np.array(int_features)]

      prediction = model.predict(final_features)[0]
      output = round(prediction, 2)

      return render_template('index.html', prediction_text='Amount of total sales: $ {}'.format(output))

if __name__ == '__main__':
  app.run(debug=True)
