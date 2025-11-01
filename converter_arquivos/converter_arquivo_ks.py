from converter_arquivos.converter_arquivo_csv_md import csv_to_markdown
from converter_arquivos.converter_arquivo_docx_md import docx_to_markdown
from converter_arquivos.converter_arquivo_excel_md import excel_to_markdown
from converter_arquivos.converter_arquivo_pdf_md import pdf_to_markdown
from converter_arquivos.converter_arquivo_txt_md import txt_to_markdown


def validar_arquivo(tipo_arquivo, nome_arquivo, pasta_saida):

    # Valida o tipo de arquivo
    if tipo_arquivo == 'csv':
        return csv_to_markdown(nome_arquivo, pasta_saida)
    elif tipo_arquivo == 'txt' or tipo_arquivo == 'text/plain':
        return txt_to_markdown(nome_arquivo, pasta_saida)
    elif tipo_arquivo == 'docx':
        return docx_to_markdown(nome_arquivo, pasta_saida)
    elif tipo_arquivo == 'xlsx':
        return excel_to_markdown(nome_arquivo, pasta_saida)
    elif tipo_arquivo == 'pdf':
        return pdf_to_markdown(nome_arquivo, pasta_saida)
    else:
        raise ValueError(f"Tipo de arquivo inválido: {tipo_arquivo}")