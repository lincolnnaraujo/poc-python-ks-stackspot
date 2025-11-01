import os
from configparser import ConfigParser

def get_property(section, key, caminho_arquivo='config.properties'):
    """Recupera o valor de uma propriedade do arquivo .properties"""
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"Arquivo de propriedades não encontrado: {caminho_arquivo}")

    config = ConfigParser()
    config.read(caminho_arquivo)

    # Verifica se a seção existe
    if not config.has_section(section):
        raise ValueError(f"Seção '{section}' não encontrada no arquivo de propriedades")

    # Verifica se a chave existe
    if not config.has_option(section, key):
        raise KeyError(f"Chave '{key}' não encontrada na seção '{section}'")

    # Retorna o valor convertido para o tipo apropriado
    try:
        # Tenta converter para inteiro
        return config.getint(section, key)
    except ValueError:
        try:
            # Tenta converter para float
            return config.getfloat(section, key)
        except ValueError:
            try:
                # Tenta converter para booleano
                return config.getboolean(section, key)
            except ValueError:
                # Retorna como string
                return config.get(section, key)


# forma de uso
#host = get_property('DATABASE', 'host')