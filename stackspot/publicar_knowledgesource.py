import json

import requests

def get_upload_data(jwt, file_name, target_id, target_type="KNOWLEDGE_SOURCE", expiration=600):
    """
    Obtém os dados necessários para realizar o upload do arquivo.
    """
    url = "https://data-integration-api.stackspot.com/v2/file-upload/form"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt}"
    }
    payload = {
        "file_name": file_name,
        "target_id": target_id,
        "target_type": target_type,
        "expiration": expiration
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200 or response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()


def upload_file(upload_data, file_path):
    """
    Realiza o upload do arquivo utilizando os dados obtidos anteriormente.
    """
    # Extraindo os dados necessários do JSON
    url = upload_data['url']
    form_data = upload_data['form']
    form_id = upload_data['id']

    print(f"upload_data: {upload_data}")
    print(f"file_path: {file_path}")
    print(f"url: {url}")
    print(f"form_data: {form_data}")
    print(f"form_id: {form_id}")

    # Preparando os dados para o envio
    files = {
        "file": open(file_path, "rb")  # Abrindo o arquivo para upload
    }
    data = {
        "key": form_data["key"],
        "x-amz-algorithm": form_data["x-amz-algorithm"],
        "x-amz-credential": form_data["x-amz-credential"],
        "x-amz-date": form_data["x-amz-date"],
        "x-amz-security-token": form_data["x-amz-security-token"],
        "policy": form_data["policy"],
        "x-amz-signature": form_data["x-amz-signature"]
    }

    # Enviando a solicitação POST
    response = requests.post(url, data=data, files=files)
    if response.status_code == 200 or response.status_code == 201 or response.status_code == 204:
        return form_id
    else:
        response.raise_for_status()


def upload_knowledge_object(upload_data_id, jwt_token, split_strategy, split_quantity, split_overlap):
    url = f"https://data-integration-api.stackspot.com/v1/file-upload/{upload_data_id}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {jwt_token}'
    }
    data = {
        "split_strategy": split_strategy,
        "split_quantity": split_quantity,
        "split_overlap": split_overlap
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
