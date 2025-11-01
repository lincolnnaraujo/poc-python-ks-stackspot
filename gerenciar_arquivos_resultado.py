import os
import shutil

from exceptions import GerenciarArquivosException

def clean_output_directory(output_dir):
    """Limpa completamente o diretório de saída"""
    try:
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        return True
    except GerenciarArquivosException as e:
        raise e
