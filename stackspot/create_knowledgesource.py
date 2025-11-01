import requests

def create_knowledge_source(api_url, api_key, nome_ks):
    """Cria um knowledge source via API."""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        "slug": nome_ks,
        "name": nome_ks,
        "description": nome_ks,
        "type": "custom"
    }

    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 409:  # Código de status para "Conflict"
        return {"message": "Knowledge Source already exists", "status_code": 409}
    elif response.status_code == 201:  # Código de status para "Created"
        return response.json()
    else:
        # Retorna a resposta completa para outros casos
        return {"message": "An error occurred", "details": response.json(), "status_code": response.status_code}