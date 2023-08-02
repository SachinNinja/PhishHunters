from flask import Flask, request, escape, jsonify, render_template, redirect
import pickle
import re
import string
import pandas as pd


model = pickle.load(open('PhishingProtector.pkl','rb'))
vector = pickle.load(open('vector.pkl', 'rb'))

app = Flask(__name__)


def preprocess_url(url):
    # Convert to lowercase
    url = str(url).lower()
    # Remove protocol prefixes
    url = re.sub(r'^https?:\/\/', '', url)
    # Remove special characters
    url = re.sub(r'[^\w\s\-\/]', '', url)
    # Remove duplicate slashes
    url = re.sub(r'\/+', '/', url)
    # Remove trailing slash
    url = url.rstrip('/')
    # Tokenize URL
    url = url.split('/')
    # Return preprocessed URL as a list of tokens
    return url


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        link = request.form['link']
        print(link)
        testing_link = {"text": [link]}
        df = pd.DataFrame(testing_link)
        df['text'] = df['text'].apply(preprocess_url)
        print(df['text'])
        df['text'] = df['text'].apply(lambda x: ' '.join(x))
        df_new = vector.transform(df['text'])
        print(df_new)
        result = model.predict(df_new)
        print(result)
        if result == 1:
            return render_template('Malicious.html')
        else: 
            return redirect(link)
       

if __name__ == '__main__':
    app.run(debug=True)
