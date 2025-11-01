import os
import pathlib
import tempfile
from pathlib import Path

import streamlit as st

from converter_arquivos.converter_arquivo_ks import validar_arquivo
from converter_arquivos.converter_url_md import url_to_markdown
from properties.recuperar_property import get_property
from stackspot.auth_stackspot_service import get_token
from stackspot.publicar_arquivos import publicar
from stackspot.create_knowledgesource import create_knowledge_source
from stackspot.clear_knowledgesource import clear_knowledge_source
from temp_file.limpar_pasta import apagar_documentos_diretorio

####################################### Sidedbar #######################################
with st.sidebar:
    pasta_documentos_convertidos = st.text_input("Caminho da pasta com ducomentos para upload:",
                                                 key="pasta_documentos_convertidos_field",
                                                 value="Downloads/arquivos_gerados_markdown")
    flag_limpar_pasta = st.checkbox(
        "Deseja apagar arquivos da pasta de arquivos convertidos?",
        help="Os arquivos da pasta serao excluidos",
        value=True
    )

####################################### Upload de arquivos #######################################
st.title("Realize a conversao de arquivos para markdown")

# Personalizando os textos do componente de upload
EXTENSOES_PERMITIDAS = ["csv", "txt", "docx", "xlsx", "pdf"]  # Lista centralizada de extensões
with st.form(key="upload_convert_file_form"):
    uploaded_file = st.file_uploader(
        label="Selecione um arquivo",
        type=EXTENSOES_PERMITIDAS,
        accept_multiple_files=False,
        help="Arraste e solte o arquivo aqui ou clique em 'Procurar arquivos'"
    )
    submit_button = st.form_submit_button(label="Enviar Arquivo")

    # Processamento do arquivo após o upload
    if uploaded_file is not None and submit_button:
        # Extrai a extensão do arquivo
        extensao = uploaded_file.name.split('.')[-1].lower() if '.' in uploaded_file.name else ""

        # Verifica se a extensão é válida
        if extensao in EXTENSOES_PERMITIDAS:
            # Mensagem geral de sucesso
            st.success("Arquivo carregado com sucesso!")

            # Mensagem específica por extensão
            st.success(f"Formato {extensao} ok!")

            # Detalhes do arquivo
            st.write("Detalhes do arquivo:")
            st.write(f"Nome do arquivo: {uploaded_file.name}")
            st.write(f"Tipo MIME: {uploaded_file.type}")
            st.write(f"Tamanho: {uploaded_file.size} bytes")

            # Processar arquivo
            caminho_saida = Path.home() / pasta_documentos_convertidos

            # Limpar pasta de saida
            if flag_limpar_pasta:
                apagar_documentos_diretorio(caminho_saida)

            # Criar arquivo temporário com extensão original
            # Obter informações do arquivo original
            nome_original = uploaded_file.name
            extensao_original = pathlib.Path(nome_original).suffix
            with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=extensao_original,
                    prefix="upload_"
            ) as tmp_file:
                # Escrever conteúdo do arquivo uploadado
                tmp_file.write(uploaded_file.getvalue())
                caminho_fisico = os.path.realpath(tmp_file.name)
                print(f"Caminho fisico: {caminho_fisico}")

            retorno_conversao_arquivo = validar_arquivo(extensao, caminho_fisico, caminho_saida)
            if retorno_conversao_arquivo == "ok":
                st.success("Arquivo convertido com sucesso!")
            else:
                st.error("Erro ao tentar converter o arquivo!")
        else:
            # Mensagem de erro para extensão inválida
            st.error("Formato de arquivo inválido!")
            st.error(f"Extensão .{extensao} não é suportada!")

st.divider()
####################################### Converter URL em arquivos #######################################
st.title("Converta sua documentacao/URL em Markdown")

with st.form("url_input_form"):
    rota_documentacao = st.text_input("Rota da sua documentacao", value="https://www.lipsum.com/")
    submit_button = st.form_submit_button("Converter em markdown")

    if rota_documentacao is not None and submit_button:
        try:
            caminho_saida = Path.home() / pasta_documentos_convertidos
            resultado = url_to_markdown(rota_documentacao, caminho_saida)
            st.success("URL convertida com sucesso!")
            st.success(f"Resultado: {resultado}")
        except Exception as e:
            st.error(f"Erro ao tentar cnverter conteudo : \n {e}")

st.divider()
####################################### Criar o KS #######################################
st.title("Publicar documentos em um knowledge source")

with st.form("ks_publicar_ks_form"):
    nome_ks = st.text_input("Nome do seu KS:", help="Slug do KS", key="nome_ks_field", value="slug-ks-custom-01")
    submit_button = st.form_submit_button("Publicar")

    if nome_ks is not None and submit_button:
        try:
            caminho_saida = Path.home() / pasta_documentos_convertidos
            url_ks = get_property('STACKSPOT', 'url_create_ks')

            # Autenticar
            token = get_token()

            # Criar KS
            resultado_criacao_ks = create_knowledge_source(url_ks, token, nome_ks)
            st.success(f"Processo de criacao finalizado com {resultado_criacao_ks}")

            # Limpar KS se necessario
            url_clear_stk = f"https://genai-code-buddy-api.stackspot.com/v1/knowledge-sources/{nome_ks}/objects"
            resultado_limpeza_ks = clear_knowledge_source(url_clear_stk ,token)
            st.success(f"Processo de limpeza do KS finalizado com {resultado_limpeza_ks}")

            # Upload de arquivos no KS
            resultado_publicacao = publicar(token, caminho_saida, nome_ks)
            st.success(f"Processo de publicacao - {resultado_publicacao}")

            st.success("Publicado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao integrar com a stackspot ao publicar KS: \n {e}")

st.divider()

####################################### Rodape #######################################
st.markdown("""
<div class="footer">
    Poc com Python + Streanlit + Stackspot • 
</div>
""", unsafe_allow_html=True)