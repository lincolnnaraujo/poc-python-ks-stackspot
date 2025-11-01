import os

import requests
import json
import re

class Context:
    def __init__(self, conversation_id, agent_built_in="true"):
        self.conversation_id = conversation_id
        self.agent_built_in = agent_built_in

class Request:
    def __init__(self, user_prompt, context):
        self.user_prompt = user_prompt
        self.context = context

def call_ai(prompt, api_key, chat_id):
    os.environ['NO_PROXY'] = 'localhost,*.localhost,*.corp1.rc.itau,*.rc.itau,*.itau.corp.ihf,*.corp.ihf,*.itau,' \
                      '*.corp.bba.com,*.cloud.ihf,*.des.ihf,*.cloudera.site,10.0.0.0/8,192.168.0.0/16,172.16.0.0/12,' \
                      '127.0.0.1 '
    os.environ['HTTP_PROXY'] = 'http://proxynew.itau:8080'
    os.environ['HTTPS_PROXY'] = 'http://proxynew.itau:8080'

    url = "https://genai-code-buddy-api.stackspot.com/v3/chat"

    context = Context(conversation_id=chat_id[:26])
    request = Request(user_prompt=prompt, context=context)
    json_data = json.dumps(request, default=lambda o: o.__dict__)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.post(url, headers=headers, data=json_data)
    response.raise_for_status()  # Levanta uma exceção para erros HTTP

    events = re.findall(r'event: (\w+)\s+data: ({.*?})\s+retry: (\d+)', response.text)

    # Transformar em lista de dicionários
    json_data = [{"event": event, "data": json.loads(data), "retry": int(retry)} for event, data, retry in events]

    # Concatenar as respostas em uma única string
    retorno = ''.join(item['data'].get('answer', '') for item in json_data)

    return retorno
