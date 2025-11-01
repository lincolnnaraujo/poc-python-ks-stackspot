# Conversor de Documentos para Markdown

## 📝 Descrição
Este projeto é uma ferramenta de conversão de documentos para o formato Markdown, com interface gráfica web utilizando Streamlit. A aplicação permite converter diversos tipos de arquivos e URLs em documentos Markdown, além de oferecer integração com a plataforma StackSpot para publicação de conhecimento.

## 🚀 Funcionalidades

### Conversão de Arquivos
- Suporte para múltiplos formatos de arquivo:
  - CSV → Markdown
  - TXT → Markdown
  - DOCX → Markdown
  - XLSX → Markdown
  - PDF → Markdown
- Conversão de URLs em documentos Markdown
- Interface web intuitiva para upload de arquivos
- Gerenciamento automático de pasta de saída

### Integração StackSpot
- Autenticação com serviços StackSpot
- Criação e gerenciamento de Knowledge Sources
- Publicação automática de arquivos convertidos
- Limpeza de Knowledge Sources existentes

## 🛠️ Tecnologias Utilizadas

### Dependências Principais
- Streamlit: Interface gráfica web
- PyPDF2: Processamento de arquivos PDF
- Pandas: Manipulação de dados tabulares
- BeautifulSoup4: Parse de HTML
- Requests: Requisições HTTP
- Docx: Processamento de documentos Word
- Openpyxl: Manipulação de planilhas Excel
- Configparser: Gerenciamento de configurações
- Jproperties: Leitura de arquivos .properties

## 📁 Estrutura do Projeto

```
├── converter_arquivos/           # Módulos de conversão de diferentes formatos
│   ├── converter_arquivo_csv_md.py
│   ├── converter_arquivo_docx_md.py
│   ├── converter_arquivo_excel_md.py
│   ├── converter_arquivo_pdf_md.py
│   ├── converter_arquivo_txt_md.py
│   └── converter_url_md.py
├── exceptions/                   # Tratamento de exceções customizadas
├── properties/                   # Gerenciamento de configurações
├── stackspot/                    # Integração com StackSpot
├── temp_file/                    # Gerenciamento de arquivos temporários
├── interface.py                  # Interface principal Streamlit
├── validacoes_url.py            # Validações de URLs
└── config.properties            # Configurações do sistema
```

## 🚦 Como Usar

1. **Preparação do Ambiente**
   - Instale as dependências: `pip install -r requirements.txt`
   - Configure o arquivo `config.properties` com suas credenciais

2. **Iniciar a Aplicação**
   - Execute o comando: `streamlit run interface.py`
   - Acesse a interface web no navegador

3. **Conversão de Arquivos**
   - Faça upload do arquivo desejado
   - Selecione as opções de conversão
   - O arquivo convertido será salvo na pasta de saída configurada

4. **Conversão de URLs**
   - Cole a URL desejada no campo específico
   - Clique em "Converter em markdown"
   - O conteúdo será convertido automaticamente

5. **Integração StackSpot**
   - Configure suas credenciais StackSpot
   - Use as funcionalidades de publicação conforme necessário

## ⚙️ Configurações

O arquivo `config.properties` permite configurar:
- Caminhos de pasta de saída
- Credenciais StackSpot
- Configurações de conversão

## 🤝 Contribuição

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
