import requests
import os
from dotenv import load_dotenv
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

api_url = f"https://grendene.agidesk.com/api/v1/issues?"

def salvarJson():
    params = {
        "app_key": os.getenv("AGIDESK_API_KEY"),
        "team": "14",
        "forecast": "teams",
        "active": "1"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Tenant-ID': 'grendene',
        'Authorization': f'Bearer {os.getenv("AGIDESK_API_KEY")}'
    }
    
    try:
        print("Making API request...")
        response = requests.get(api_url, params=params, headers=headers, verify=False)
        response.raise_for_status()
        
        data = response.json()
        print(f"Received data: {data}")
        
        file_path = 'chamados.json'
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
            
        print(f"File saved at: {os.path.abspath(file_path)}")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error making the request: {str(e)}")
        raise
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {str(e)}")
        raise
    except IOError as e:
        print(f"Error saving file: {str(e)}")
        raise

if __name__ == "__main__":
    result = salvarJson()    