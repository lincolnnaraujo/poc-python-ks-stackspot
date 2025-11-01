import time

import requests

from properties.recuperar_property import get_property

url_request = (get_property('STACKSPOT', 'url_auth_base')
               + get_property('STACKSPOT', 'auth_realm')
               + get_property('STACKSPOT', 'url_auth_complement'))

class ResponseData:
    def __init__(self):
        self.access_token = ""
        self.refresh_token = ""
        self.obtained_at = None

response_data = ResponseData()

def get_token():

    client_id = get_property('STACKSPOT', 'client_id')
    client_secret = get_property('STACKSPOT', 'client_secret')

    if not response_data.access_token:
        return request_token({
            "client_id": client_id,
            "grant_type": "client_credentials",
            "client_secret": client_secret
        })

    if time.time() - response_data.obtained_at < 10 * 60:
        return response_data.access_token

    return do_refresh_token(response_data.refresh_token)

def do_refresh_token(refresh_token):
    return request_token({
        "refresh_token": refresh_token,
        "client_id": "stackspot-portal-ai",
        "grant_type": "refresh_token",
        "redirect_uri": "https://ai.stackspot.com/"
    })

def request_token(form_data):
    try:
        response = requests.post(url_request, data=form_data, headers={
            "Content-Type": "application/x-www-form-urlencoded"
        })
        response.raise_for_status()
        data = response.json()
        response_data.access_token = data.get("access_token", "")
        response_data.refresh_token = data.get("refresh_token", "")
        response_data.obtained_at = time.time()
        return response_data.access_token
    except requests.RequestException as e:
        print(f"Erro ao enviar a solicitação: {e}")
        raise e
    except ValueError as e:
        print(f"Erro ao decodificar o JSON da resposta: {e}")
        raise e