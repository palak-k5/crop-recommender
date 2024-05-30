import joblib
import numpy as np
from flask import Flask, request, jsonify, render_template
import os
import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
openai.api_key  = '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'
# print(openai.api_key)


app = Flask(__name__)
model = None
scaler = None

try:
    # model = joblib.load('final_model.joblib')
    model = joblib.load('model.joblib')
    # scaler = joblib.load('final_scaler.joblib')
except Exception as e:
    print("Error loading model or scaler:", str(e))

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == "POST":
        try:
            features = [float(x) for x in request.form.values()]
            input_data = np.array(features).reshape(1, -1)
            # if scaler is not None:
                # scaled_features = scaler.transform(input_data)
            prediction = model.predict(input_data)
            output = prediction[0]
            return render_template('result.html', prediction_text=output)
            # else:
                # return render_template('error.html', error_message='Scaler not loaded.')
        except Exception as e:
            return render_template('error.html', error_message=str(e))
    else:
        return render_template('index.html')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    try:
        data = request.get_json(force=True)
        # if model is not None or scaler is not None:
        input_data = np.array(list(data.values())).reshape(1, -1)
            # scaled_features = scaler.transform(input_data)
        prediction = model.predict(input_data)
        output = prediction[0]
        return jsonify({'prediction': output})
        # else:
            # return jsonify({'error': 'Model or scaler not loaded.'})
    except Exception as e:
        return jsonify({'error': str(e)})

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0.5):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    #     print(str(response.choices[0].message))
    return response

context = [ {'role':'system', 'content':"""
You are ChatBot, an automated service to related to farming in indian context. \
You first greet the customer, then ask about the crop they want to grow. \
and them ask user bydiplaying list they want to know about the \
1. investment scope of the crop for standard resources and profit margin \
2. threats of crop \ 
3. Soil nutrient of which user want help to test \
4. any other query \
and then asks if it's a home garden or farm. \
You wait to collect the response, then summarize it and suggest according to it \
and then ask for more assisstance if they need \
You respond in a short, very conversational friendly style. \
The nutrients includes \
nitrogen \
phosphorous \
potassium \
ph value \
"""} ]  # accumulate messages


@app.route('/chatbot', methods=['POST'])
def response():
    user_input = request.json['user_input']
    context.append({'role':'user', 'content':f"{user_input}"})
    response = get_completion_from_messages(context)
    print(response.choices[0].message["content"])

    context.append({'role':'assistant', 'content':f"{response}"})
    return jsonify({'response':response.choices[0].message["content"]})
    


if __name__ == "__main__":
    app.run()
