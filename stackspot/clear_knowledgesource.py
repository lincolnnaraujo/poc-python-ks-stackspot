import requests

def clear_knowledge_source(api_url, api_key):
    """Cria um knowledge source via API."""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    response = requests.delete(api_url, headers=headers)

    if response.status_code == 204:  # Objeto deletado com sucesso
        return "Processo finalizado"
    else:
        # Retorna a resposta completa para outros casos
        return {"message": "An error occurred", "details": response.json(), "status_code": response.status_code}