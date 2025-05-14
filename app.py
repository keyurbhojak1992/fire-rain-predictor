from flask import Flask, render_template, request
import joblib
import pandas as pd

# Load the trained model
model = joblib.load('random_forest_model.pkl')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get input values from the user
    temperature = float(request.form['Temperature'])
    rh = float(request.form['RH'])
    ws = float(request.form['Ws'])
    rain = float(request.form['Rain'])
    ffmc = float(request.form['FFMC'])
    dmc = float(request.form['DMC'])
    dc = float(request.form['DC'])
    isi = float(request.form['ISI'])
    bui = float(request.form['BUI'])
    fwi = float(request.form['FWI'])

    # Prepare the input data
    input_data = pd.DataFrame([[temperature, rh, ws, rain, ffmc, dmc, dc, isi, bui, fwi]],
                              columns=['Temperature', 'RH', 'Ws', 'Rain', 'FFMC', 'DMC', 'DC', 'ISI', 'BUI', 'FWI'])

    # Make a prediction
    prediction = model.predict(input_data)

    # Output the result
    if prediction[0] == 0:
        result = 'No Fire'
    else:
        result = 'Fire'

    return render_template('index.html', prediction_text='Prediction: {}'.format(result))

if __name__ == "__main__":
    app.run(debug=True)

def ping_self():
    while True:
        try:
            # Ping your own Render URL every 5 minutes
            requests.get("https://your-app-name.onrender.com")
            sleep(300)  # 300 seconds = 5 minutes
        except:
            sleep(60)  # If error, wait 1 minute and retry

# Start keep-alive thread when not in debug mode
if not app.debug and os.environ.get("WERKZEUG_RUN_MAIN") != "true":
    t = Thread(target=ping_self)
    t.daemon = True
    t.start()

if __name__ == '__main__':
    app.run(debug=True)
