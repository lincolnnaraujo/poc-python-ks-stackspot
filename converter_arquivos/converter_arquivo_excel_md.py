import pandas as pd
import os
import re
from pathlib import Path
from datetime import datetime


def excel_to_markdown(caminho_planilha, pasta_saida):
    """
    Converte cada aba de uma planilha Excel (.xls ou .xlsx) em arquivos Markdown separados.
    Nome dos arquivos: <nome_aba>_<timestamp>.md

    Args:
        caminho_planilha (str): Caminho do arquivo Excel (.xls ou .xlsx)
        pasta_saida (str, opcional): Pasta para salvar os arquivos Markdown.
            Padrão: mesma pasta do arquivo Excel.
    """
    try:
        # Verificar se o arquivo existe e tem extensão válida
        if not os.path.isfile(caminho_planilha):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_planilha}")

        # Cria o diretório de saída se não existir
        os.makedirs(pasta_saida, exist_ok=True)

        # Verificar extensão do arquivo
        extensao = os.path.splitext(caminho_planilha)[1].lower()
        if extensao not in ['.xls', '.xlsx']:
            raise ValueError(f"Formato não suportado: {extensao}. Use .xls ou .xlsx")

        # Definir pasta de saída padrão
        if pasta_saida is None:
            pasta_saida = os.path.dirname(caminho_planilha)

        # Criar pasta de saída se não existir
        Path(pasta_saida).mkdir(parents=True, exist_ok=True)

        # Obter timestamp global para todos os arquivos
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Ler todas as abas do Excel
        try:
            # Usar engine apropriada para cada formato
            engine = 'openpyxl' if extensao == '.xlsx' else None
            planilha = pd.read_excel(caminho_planilha, sheet_name=None, engine=engine)
        except Exception as e:
            raise ValueError(f"Erro ao ler o arquivo Excel: {str(e)}")

        # Processar cada aba
        for nome_aba, dados in planilha.items():
            # Gerar nome do arquivo seguro com timestamp
            nome_seguro = sanitizar_nome_arquivo(nome_aba)
            nome_arquivo = f"{nome_seguro}_{timestamp}.md"
            caminho_completo = os.path.join(pasta_saida, nome_arquivo)

            # Converter para Markdown
            try:
                # Verificar se o DataFrame não está vazio
                if dados.empty:
                    print(f"Aviso: A aba '{nome_aba}' está vazia. Nenhum arquivo será criado.")
                    continue

                md_tabela = dados.to_markdown(index=False)
                with open(caminho_completo, 'w', encoding='utf-8') as f:
                    f.write(f"# {nome_aba}\n\n")
                    f.write(md_tabela)
                print(f"Arquivo criado: {nome_arquivo}")
            except Exception as e:
                print(f"Erro na aba '{nome_aba}': {str(e)}")
                raise e

        return "ok"
    except Exception as e:
        raise e


def sanitizar_nome_arquivo(nome):
    """Remove caracteres inválidos e formata nome de arquivo"""
    # Remover caracteres específicos problemáticos
    nome = re.sub(r'[<>:"/\\|?*]', '', nome)

    # Substituir espaços e caracteres especiais por underscore
    nome = re.sub(r'[\s\u200b]+', '_', nome)

    # Remover trailing underscores e pontos
    nome = nome.strip('_.')

    # Limitar tamanho do nome (máx 100 caracteres)
    nome = nome[:100]

    # Garantir que o nome não fique vazio
    return nome if nome else "aba"