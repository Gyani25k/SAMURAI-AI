from flask import Flask, jsonify, request
import requests
import ast
import os
import openai
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# GEMINI AI API CONFIGURATION
GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
GEMINI_MODEL = genai.GenerativeModel('gemini-pro')

# GPT AI API CONFIGURATION
GPT_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = GPT_API_KEY
GPT4_MODEL = "gpt-4"
GPT_MODEL = "gpt-3.5-turbo"

# BASE URL
URL = 'http://samurai3.keenetic.link/csv/ai_new_queue.php'

# Function to get data from URL with pagination
def get_data(url, offset, limit):
    try:
        params = {'offset': offset, 'limit': limit}
        with requests.get(url, params=params) as response:
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                return {"error": "Failed to fetch data", "site_status": response.status_code}
    except Exception as e:
        return {"error": str(e), "site_status": 500}
    

# Function to get response via Gemini model
def get_gemini_response(user_prompt):
    try:
        response = GEMINI_MODEL.generate_content(user_prompt)
        result = str(response.parts[0])
        extracted_text = ast.literal_eval(result.split(':', 1)[1].strip())
        return extracted_text
    except Exception as e:
        return str(e)


# Function to get response via GPT model
def get_openai_response(user_prompt):
    try:
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[
                {"role": "user", "content": user_prompt},
            ]
        )
        data1 = dict(response)
        data2 = dict(data1['choices'][0])
        data3 = dict(data2['message'])
        return data3['content']
    except Exception as e:
        return str(e)
    
# Function to get response via GPT model
def get_openai_response_GPT4(user_prompt):
    try:
        response = openai.ChatCompletion.create(
            model=GPT4_MODEL,
            messages=[
                {"role": "user", "content": user_prompt},
            ]
        )
        data1 = dict(response)
        data2 = dict(data1['choices'][0])
        data3 = dict(data2['message'])
        return data3['content']
    except Exception as e:
        return str(e)

@app.route('/getAllResponseFromAI', methods=['GET'])
def get_response_from_ai():
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 100))
    
    data = get_data(URL, offset, limit)
    
    if 'error' in data:
        return jsonify({"error": "Failed to fetch data"}), 500

    task_list = data['list']['data']
    responses = []

    for item in task_list:
        print(item['id'])
        print(item['job_id'])
        modified_prompt = data['prompt']
        if 'column1' not in modified_prompt and 'column2' not in modified_prompt:
            modified_prompt += f" {item['column1']} & {item['column2']}"
        else:
            modified_prompt = modified_prompt.replace('column1', item['column1']).replace('column2', item['column2'])

        if data['use'] == 'Gemini':
            response = get_gemini_response(modified_prompt)
        if data['use'] == 'GPT3':
            response = get_openai_response(modified_prompt)
        if data['use'] == 'GPT4':
            response = get_openai_response_GPT4(modified_prompt)
            pass
        
        print(response)
        responses.append({'job_id':item['job_id'],'id': item['id'], 'response': response})

    url_to_send = 'http://samurai3.keenetic.link/csv/ai_new_endpoint.php'
    response = requests.post(url_to_send, json=responses)

    return jsonify(responses)

@app.route('/getthreeResponseFromAI', methods=['GET'])
def get_response_from_ai_preview():
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 3))
    
    data = get_data(URL, offset, 3)
    
    if 'error' in data:
        return jsonify({"error": "Failed to fetch data"}), 500

    task_list = data['list']['data']
    responses = []

    for item in task_list:
        print(item['id'])
        print(item['job_id'])
        modified_prompt = data['prompt']
        if 'column1' not in modified_prompt and 'column2' not in modified_prompt:
            modified_prompt += f" {item['column1']} & {item['column2']}"
        else:
            modified_prompt = modified_prompt.replace('column1', item['column1']).replace('column2', item['column2'])

        if data['use'] == 'Gemini':
            response = get_gemini_response(modified_prompt)
        if data['use'] == 'GPT3':
            response = get_openai_response(modified_prompt)
        if data['use'] == 'GPT4':
            response = get_openai_response_GPT4(modified_prompt)
            pass
        
        print(response)
        responses.append({'job_id':item['job_id'],'id': item['id'], 'response': response})

    url_to_send = 'http://samurai3.keenetic.link/csv/ai_new_endpoint.php'
    response = requests.post(url_to_send, json=responses)

    return jsonify(responses)


@app.route('/getFifteenResponseFromAI', methods=['GET'])
def get_response_from_ai_fifteen():
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 15))
    
    data = get_data(URL, offset, 15)
    
    if 'error' in data:
        return jsonify({"error": "Failed to fetch data"}), 500

    task_list = data['list']['data']
    responses = []

    for item in task_list:
        print(item['id'])
        print(item['job_id'])
        modified_prompt = data['prompt']
        if 'column1' not in modified_prompt and 'column2' not in modified_prompt:
            modified_prompt += f" {item['column1']} & {item['column2']}"
        else:
            modified_prompt = modified_prompt.replace('column1', item['column1']).replace('column2', item['column2'])

        if data['use'] == 'Gemini':
            response = get_gemini_response(modified_prompt)
        if data['use'] == 'GPT3':
            response = get_openai_response(modified_prompt)
        if data['use'] == 'GPT4':
            response = get_openai_response_GPT4(modified_prompt)
            pass
        
        print(response)
        responses.append({'job_id':item['job_id'],'id': item['id'], 'response': response})

    url_to_send = 'http://samurai3.keenetic.link/csv/ai_new_endpoint.php'
    
    response = requests.post(url_to_send, json=responses)

    return jsonify(responses)


if __name__ == '__main__':
    app.run(debug=True)
