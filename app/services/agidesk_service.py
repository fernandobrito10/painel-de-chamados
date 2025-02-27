import requests
import os
from dotenv import load_dotenv
import urllib3
from typing import Tuple, List, Dict, Any
from datetime import datetime, timedelta
from functools import lru_cache

class AgideskService:

    def __init__(self):
        load_dotenv()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        self.api_url = "https://grendene.agidesk.com/api/v1/issues"
        self.api_key = os.getenv("AGIDESK_API_KEY")
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Tenant-ID": "grendene",
            "Authorization": f"Bearer {self.api_key}"
        }
        self.cache_timeout = 300  # 5 minutos em segundos

    def get_tickets_count(self) -> Tuple[int, int]:
        params = {
            "app_key": self.api_key,
            "team": "14",
            "forecast": "teams",
            "active": "1"
        }
        
        try:
            response = requests.get(
                self.api_url, 
                params=params, 
                headers=self.headers, 
                verify=False
            )
            response.raise_for_status()
            
            data = response.json()
            tickets_with_responsible = [
                task for task in data 
                if task.get('responsible_id')
            ]
            tickets_without_responsible = [
                task for task in data 
                if not task.get('responsible_id')
            ]
            
            return len(tickets_with_responsible), len(tickets_without_responsible)
            
        except requests.exceptions.RequestException as e:
            print(f"Error in API request: {str(e)}")
            raise

    @lru_cache(maxsize=1)
    def get_all_tickets(self) -> List[Dict[str, Any]]:
        """Cache dos tickets por 5 minutos"""
        params = {
            "app_key": self.api_key,
            "team": "14",
            "forecast": "teams",
            "active": "1"
        }
        
        try:
            response = requests.get(
                self.api_url, 
                params=params, 
                headers=self.headers, 
                verify=False
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error in API request: {str(e)}")
            raise

    def clear_cache(self):
        """Limpa o cache de tickets"""
        self.get_all_tickets.cache_clear()


def main():
    service = AgideskService()
    with_responsible, without_responsible = service.get_tickets_count()
    total_tickets = with_responsible + without_responsible
    
    print(f"Number of tickets with responsible: {with_responsible}")
    print(f"Number of tickets without responsible: {without_responsible}")
    print(f"Total number of tickets: {total_tickets}")


if __name__ == "__main__":
    main()
