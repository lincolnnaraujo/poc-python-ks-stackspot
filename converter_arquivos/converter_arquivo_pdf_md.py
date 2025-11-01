import os
import re
from datetime import datetime

import PyPDF2


def pdf_to_markdown(input_file, output_dir):

    try:
        # Cria o diretório de saída se não existir
        os.makedirs(output_dir, exist_ok=True)

        base_name = os.path.basename(input_file)
        file_name = re.sub(r'[\\/*?:"<>|]', '', os.path.splitext(base_name)[0])[:50]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{file_name}_{timestamp}.md"
        output_path = os.path.join(output_dir, output_file)

        texto_pdf = extrair_texto_pdf(input_file)
        escrever_markdown(texto_pdf, output_path)

        return "ok"
    except Exception as e:
        raise e

# Função para extrair texto de PDF
def extrair_texto_pdf(arquivo):
    leitor = PyPDF2.PdfReader(arquivo)
    texto = ""
    for pagina in leitor.pages:
        texto += pagina.extract_text()
    return texto

# Função para escrever o texto extraído em um arquivo Markdown
def escrever_markdown(conteudo, arquivo_md):
    with open(arquivo_md, 'w', encoding='utf-8') as f:
        f.write(conteudo)
