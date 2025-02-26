import requests
import os
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

api_url = "https://grendene.agidesk.com/api/v1/issues?"

def contarChamados():
    params = {
        "app_key": os.getenv("AGIDESK_API_KEY"),
        "team": "14",
        "forecast": "teams",
        "active": "1"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Tenant-ID": "grendene",
        "Authorization": f"Bearer {os.getenv('AGIDESK_API_KEY')}"
    }
    
    try:
        response = requests.get(api_url, params=params, headers=headers, verify=False)
        response.raise_for_status()
        
        data = response.json()
        chamados_sem_responsavel = [task for task in data if not task.get('responsible_id')]
        chamados_com_responsavel = [task for task in data if task.get('responsible_id')]
        
        return len(chamados_com_responsavel), len(chamados_sem_responsavel)
        
    except requests.exceptions.RequestException as e:
        print(f"Erro no request: {str(e)}")
        raise

if __name__ == "__main__":
    chamados_com_responsavel, chamados_sem_responsavel = contarChamados()
    chamados_totais = chamados_com_responsavel + chamados_sem_responsavel
    print(f"Número de chamados com responsável: {chamados_com_responsavel}")
    print(f"Número de chamados sem responsável: {chamados_sem_responsavel}")
    print(f"Número total de chamados: {chamados_totais}")
