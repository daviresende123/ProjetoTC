# Pré-requisitos
Antes de começar, certifique-se de ter o seguinte instalado em sua máquina:

1. **Python 3.7+**: A API foi desenvolvida em Python e requer uma versão compatível. Você pode verificar sua versão do Python executando `python --version` no terminal.
2. **Git**: Necessário para clonar o repositório. Você pode verificar se o Git está instalado executando `git --version`. Caso não esteja, você pode baixá-lo em [https://git-scm.com/](https://git-scm.com/).

# Clonando o repositório
1. Abra o terminal na pasta onde você deseja salvar o projeto.
2. Execute o seguinte comando para clonar o repositório:
   ```bash
   git clone https://github.com/daviresende123/ProjetoTC.git
3.Após a clonagem, acesse o diretório do projeto: cd <nome do diretório do seu projeto>

# Criando e ativando o ambiente virtual
1.Dentro do diretório do projeto, crie um ambiente virtual (recomendado para isolar as dependências do projeto):
    Linux/macOS: `python3 -m venv venv`
    Windows: `python -m venv venv`
    
2.Ative o ambiente virtual:
    Linux/macOS: `source venv/bin/activate`
    Windows: `venv\Scripts\activate`


# Instalando as dependências
1.Com o ambiente virtual ativado, instale as dependências do projeto a partir do arquivo requirements.txt:
    `pip install -r requirements.txt`


# Executando a API
1.Após a instalação das dependências, você pode executar a API usando o Uvicorn:
    `uvicorn main:app --reload`
2.Abra o seu navegador e acesse http://127.0.0.1:8000/docs#/ para interagir com a API
