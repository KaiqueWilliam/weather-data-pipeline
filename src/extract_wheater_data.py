import requests
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_weather_data_pipe(url: str) -> dict:
    try:
        response = requests.get(url)

        if response.status_code != 200:
            logging.error(f"Erro na requisição. Status: {response.status_code}. Resposta: {response.text}")
            return {}
        
        data = response.json()

        if not data:
            logging.warning("Nenhum dado retornado.")
            return {}

        output_path = 'data/weather_data.json'
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)

        logging.info(f"Arquivo salvo em {output_path}")
        return data

    except requests.exceptions.RequestException as e:
        logging.error(f"Erro de conexão ao tentar acessar a API: {e}")
        return {}
    except ValueError as e:
        logging.error(f"Erro ao decodificar o JSON: {e}")
        return {}

