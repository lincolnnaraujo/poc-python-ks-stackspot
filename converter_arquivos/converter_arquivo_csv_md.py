import csv
import os
import re
from datetime import datetime


def csv_to_markdown(input_file, output_dir, delimiter=None):
    try:
        # Cria o diretório de saída se não existir
        os.makedirs(output_dir, exist_ok=True)

        with open(input_file, 'r') as csvfile:
            # Tentativa de detecção do delimitador
            sample = csvfile.read(2048)
            csvfile.seek(0)

            # Usa delimitador fornecido ou tenta detectar automaticamente
            if delimiter:
                chosen_delimiter = delimiter
            else:
                # Verifica delimitadores candidatos na amostra
                delimiter_candidates = [';', ',', '\t', '|']
                counts = {delim: sample.count(delim) for delim in delimiter_candidates}

                # Escolhe o delimitador com maior frequência (ignorando zero)
                chosen_delimiter = max(counts, key=counts.get) if any(counts.values()) else ','

                # Validação adicional para CSVs com apenas 1 coluna
                if not any(counts.values()) or len(sample.splitlines()[0].split(chosen_delimiter)) < 2:
                    raise ValueError("Não foi possível detectar o delimitador automaticamente")

            # Processa o arquivo CSV
            reader = csv.reader(csvfile, delimiter=chosen_delimiter)
            rows = []
            for row in reader:
                if any(field.strip() for field in row):  # Ignora linhas vazias
                    rows.append(row)

            if not rows:
                raise ValueError("Arquivo CSV vazio ou sem dados válidos")

            # Processa os dados para Markdown
            markdown_rows = []
            for i, row in enumerate(rows):
                # Escapa pipes e quebras de linha
                processed_row = [str(cell).replace('|', '\\|').replace('\n', '<br>') for cell in row]
                markdown_rows.append(processed_row)

                # Adiciona separador de cabeçalho após a primeira linha
                if i == 0:
                    header_separator = ['---' for _ in row]
                    markdown_rows.append(header_separator)

            # Formata as linhas como tabela Markdown
            markdown_lines = ['| ' + ' | '.join(row) + ' |' for row in markdown_rows]
            markdown_table = '\n'.join(markdown_lines)

            # Gerar nome do arquivo de saída
            base_name = os.path.basename(input_file)
            file_name = re.sub(r'[\\/*?:"<>|]', '', os.path.splitext(base_name)[0])[:50]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{file_name}_{timestamp}.md"
            output_path = os.path.join(output_dir, output_file)

            # Salvar arquivo Markdown
            with open(output_path, 'w', encoding='utf-8') as md_file:
                md_file.write(markdown_table)

            return "ok"
    except Exception as e:
        print(f"ERRO: {e}")
        raise
