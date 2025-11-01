import os
import re
from datetime import datetime


def txt_to_markdown(input_file, output_dir):
    """
        Converte um arquivo texto (.txt) para Markdown (.md) com formatação básica

        Parâmetros:
        input_file (str): Caminho do arquivo TXT de entrada
        output_file (str): Caminho do arquivo Markdown de saída
        """
    markdown_lines = []

    try:

        # Cria o diretório de saída se não existir
        os.makedirs(output_dir, exist_ok=True)

        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                stripped = line.strip()

                # Ignora linhas vazias
                if not stripped:
                    continue

                # Detecta títulos (linhas com sublinhado)
                if line.startswith('===') or line.startswith('---'):
                    if markdown_lines:
                        markdown_lines[-1] = f"### {markdown_lines[-1]}"
                    continue

                # Detecta listas
                if stripped.startswith('- ') or stripped.startswith('* '):
                    markdown_lines.append(f"- {stripped[2:]}")
                    continue

                # Detecta blocos de código
                if stripped.startswith('```'):
                    markdown_lines.append("```")
                    continue

                # Adiciona parágrafos
                markdown_lines.append(stripped)

        # Junta parágrafos com quebras de linha duplas
        content = "\n\n".join(markdown_lines)

        # Gerar nome do arquivo de saída
        base_name = os.path.basename(input_file)
        file_name = re.sub(r'[\\/*?:"<>|]', '', os.path.splitext(base_name)[0])[:50]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{file_name}_{timestamp}.md"
        output_path = os.path.join(output_dir, output_file)

        with open(output_path, 'w', encoding='utf-8') as md_file:
            md_file.write(content)

        return "ok"
    except Exception as e:
        raise e