import ast
import os
import openai
import requests
from flask import Flask,jsonify
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


# GEMINI AI API CONFRIGUATION

GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

GEMINI_MODEL = genai.GenerativeModel('gemini-pro')

# GPT AI API CONFRIGUATION

GPT_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = GPT_API_KEY

GPT_MODEL = "gpt-3.5-turbo"


# BASE URL

URL = 'http://samurai3.keenetic.link/csv/ai_new_queue.php?check=1'


# FUNCTION TO GET DATA FROM URL

def get_data(url):
    try:
        with requests.get(url) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                except ValueError:
                    return {"error": "Invalid JSON response", "site_status": response.status_code}
                else:
                    return data
            else:
                return {"site_status": response.status_code}
            
    except Exception as e:
        return {"error": str(e), "site_status": 500}
    
# FUNCTION TO GET RESPONSE VIA GEMINI MODEL

def get_gemini_response(user_prompt):
    extracted_text = ''
    try:
        response = GEMINI_MODEL.generate_content(user_prompt)
        result = str(response.parts[0])
        extracted_text = ast.literal_eval(result.split(':', 1)[1].strip())

    except Exception as e:
        extracted_text = str(e)

    return extracted_text        

# FUNCTION TO GET RESPONSE VIA GPT MODEL

def get_openai_response(user_prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_prompt},
        ]
    )
    data1 = dict(response)
    data2 = dict(data1['choices'][0])
    data3 = dict(data2['message'])

    return data3['content']



@app.route('/getResponseFromAI')
def getResponseFromAI():
    data = get_data(URL)

    if data['use'] == 'Gemini':
        list_data = data['list']['data']
        modified_prompts = {}

        for item in list_data:
            modified_prompt = data['prompt'].replace('column1', item['column1']).replace('column2', item['column2'])
            modified_prompts[item['id']] = modified_prompt

        result_list = []

        for id, prompt in modified_prompts.items():
            response = get_gemini_response(prompt)
            result_list.append({'id': id, 'response': response})

        url_to_send = 'http://samurai3.keenetic.link/csv/ai_new_endpoint.php'

        response = requests.post(url_to_send, json=result_list)

        return jsonify(result_list)
    
    else:

        list_data = data['list']['data']
        modified_prompts = {}

        for item in list_data:
            modified_prompt = data['prompt'].replace('column1', item['column1']).replace('column2', item['column2'])
            modified_prompts[item['id']] = modified_prompt

        result_list = []

        for id, prompt in modified_prompts.items():
            print(id)
            response = get_openai_response(prompt)
            result_list.append({'id': id, 'response': response})

        url_to_send = 'http://samurai3.keenetic.link/csv/ai_new_endpoint.php'

        response = requests.post(url_to_send, json=result_list)


        return jsonify(result_list)


if __name__ == '__main__':
    app.run(debug=True)