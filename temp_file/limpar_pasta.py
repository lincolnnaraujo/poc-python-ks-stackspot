import os
import shutil


def apagar_documentos_diretorio(output_dir):
    """Limpa completamente o diretório de saída"""
    try:
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        return True
    except Exception as e:
        raise e
