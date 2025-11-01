# Formatar URLs Markdown

## Visão Geral

Este projeto oferece uma interface baseada em Streamlit para converter diversos formatos de documentos e URLs em Markdown, gerenciar arquivos convertidos e integrar com a plataforma Knowledge Source (KS) da Stackspot. Suporta upload de arquivos, conversão de URLs e publicação de documentos na Stackspot, além de um chat simulado.

---

## Estrutura de Diretórios

- `interface.py`: Aplicação principal Streamlit, interface do usuário e orquestração do fluxo.
- `converter_arquivos/`: Módulos para conversão de diferentes tipos de arquivos (CSV, DOCX, XLSX, PDF, TXT, URLs) para Markdown.
- `exceptions/`: Classes de exceção personalizadas.
- `properties/`: Utilitários para leitura de propriedades de configuração.
- `stackspot/`: Integração com serviços da Stackspot (autenticação, criação de KS, publicação de arquivos).
- `temp_file/`: Utilitários para gerenciamento e limpeza de arquivos temporários.
- `pymock/`: Implementações mock para Stackspot e processamento de PDF (para testes/desenvolvimento).
- `config.properties`: Arquivo de configuração.
- `requirements.txt`: Dependências Python.

---

## Funcionalidades Principais

### 1. Upload e Conversão de Arquivos

- Usuários podem fazer upload de arquivos (`csv`, `txt`, `docx`, `xlsx`, `pdf`).
- Os arquivos são validados e convertidos para Markdown usando o conversor apropriado em `converter_arquivos/`.
- Os arquivos convertidos são salvos em um diretório especificado pelo usuário.
- Opção para limpar o diretório de saída antes de salvar novos arquivos.

### 2. Conversão de URL para Markdown

- Usuários podem informar uma URL de documentação.
- O conteúdo da URL é buscado e convertido para Markdown usando `converter_arquivos/converter_url_md.py`.
- O resultado é salvo no diretório de saída.

### 3. Publicação no Knowledge Source da Stackspot

- Usuários podem especificar o nome do KS (Knowledge Source).
- A aplicação autentica na Stackspot, faz upload dos arquivos convertidos e publica no KS informado.
- Utiliza módulos em `stackspot/` para autenticação, criação de KS e publicação.

### 4. Chat com Stackspot (Simulado)

- Usuários podem enviar mensagens para um assistente simulado da Stackspot.
- As mensagens são exibidas com timestamp na interface.

---

## Principais Módulos

- **`converter_arquivos/`**: Lógica para conversão de cada tipo de arquivo suportado para Markdown.
- **`stackspot/`**: Autenticação, criação de KS e publicação de arquivos na Stackspot.
- **`properties/`**: Leitura de valores de configuração do `config.properties`.
- **`temp_file/`**: Funções para limpeza de diretórios temporários ou de saída.

---

## Como Usar

1. **Instale as dependências**:
   `pip install -r requirements.txt`

2. **Execute a aplicação**:
   `streamlit run interface.py`

3. **Siga a interface**:
   - Faça upload de arquivos ou informe uma URL para converter em Markdown.
   - Opcionalmente, publique os arquivos convertidos na Stackspot.
   - Use o chat para interação simulada.

---

## Configuração

- Edite o arquivo `config.properties` para definir URLs da Stackspot e outras propriedades conforme necessário.

---

## Observações

- O chat é apenas uma simulação e não conecta a um assistente real.
- Os módulos mock em `pymock/` são para desenvolvimento/testes e não devem ser usados em produção.

---