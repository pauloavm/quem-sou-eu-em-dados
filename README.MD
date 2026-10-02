# Quem sou eu em Dados? 📊

> 🎯 **Sobre o Projeto:** Uma aplicação interativa desenvolvida em Python e Streamlit que avalia as suas competências técnicas e determina o seu perfil ideal no ecossistema de dados (Analista, Cientista, Engenheiro de Dados ou ML Engineer). O sistema gera gráficos de radar dinâmicos, integra-se ao Supabase para armazenamento seguro e exporta relatórios executivos em PDF com recomendações de estudo.

## 🚀 Funcionalidades

*   **Avaliação de Habilidades:** Formulário dinâmico com 10 competências essenciais do mercado de dados.
*   **Seleção em Cascata:** Integração com API externa para seleção precisa de País > Estado > Cidade.
*   **Algoritmo de *Match*:** Cálculo de similaridade (distância euclidiana) entre o perfil do usuário e os padrões da indústria.
*   **Visualização de Dados:** Geração de gráficos de radar interativos (Plotly) sobrepondo o perfil do usuário ao perfil ideal.
*   **Exportação de Relatório (PDF):** Geração de um documento executivo formatado com os resultados, gráfico integrado e hiperligações para recursos de estudo gratuitos.
*   **Armazenamento em Nuvem:** Integração direta com o banco de dados Supabase para registro contínuo dos resultados.

## 🛠️ Tecnologias Utilizadas

*   **Linguagem:** Python 3.13
*   **Framework Web:** Streamlit
*   **Visualização:** Plotly, Kaleido (renderização de imagens estáticas)
*   **Geração de PDF:** FPDF
*   **Banco de Dados:** Supabase (PostgreSQL)
*   **Integrações:** API CountriesNow (Geolocalização)

## 📂 Estrutura do Repositório

O projeto possui uma estrutura minimalista e direta:
*   `app.py`: Código-fonte principal contendo a interface, lógica de cálculo e geração do PDF.
*   `requirements.txt`: Lista de dependências do Python necessárias para rodar o projeto.
*   `.gitignore`: Arquivo de exclusão para evitar o versionamento de pastas locais (como `venv/`) e credenciais sensíveis.

## 💻 Como Executar Localmente (Passo a Passo)

Siga estas instruções para rodar o projeto na sua própria máquina.

### 1. Clonar o Repositório
Abra o seu terminal (Prompt de Comando, PowerShell ou Git Bash) e execute:
```bash
git clone [https://github.com/pauloavm/quem-sou-eu-em-dados.git](https://github.com/pauloavm/quem-sou-eu-em-dados.git)
cd quem-sou-eu-em-dados

```

### 2. Criar e Ativar o Ambiente Virtual

O ambiente virtual isola as bibliotecas deste projeto das restantes do seu computador.

```bash
# Criar o ambiente
python -m venv venv

# Ativar no Windows
venv\Scripts\activate

# Ativar no Linux / Mac
source venv/bin/activate

```

*(Após a ativação, você verá o prefixo `(venv)` no seu terminal).*

### 3. Instalar as Dependências

Com o ambiente ativado, instale as bibliotecas listadas no arquivo de requisitos:

```bash
pip install -r requirements.txt

```

### 4. Configurar as Credenciais do Banco de Dados (Supabase)

O projeto requer conexão com o Supabase para armazenar os formulários.

1. Crie uma pasta oculta chamada `.streamlit` na raiz do projeto:
```bash
mkdir .streamlit

```


2. Dentro desta pasta, crie um arquivo chamado `secrets.toml`.
3. Adicione as suas chaves do Supabase neste arquivo com o seguinte formato:
```toml
SUPABASE_URL = "[https://sua-url-do-projeto.supabase.co](https://sua-url-do-projeto.supabase.co)"
SUPABASE_KEY = "sua_chave_publishable_aqui"

```


*Nota: O arquivo `.gitignore` já está configurado para nunca enviar o `secrets.toml` para o GitHub.*

### 5. Executar a Aplicação

Inicie o servidor local do Streamlit:

```bash
streamlit run app.py

```

O seu navegador abrirá automaticamente uma nova aba no endereço `http://localhost:8501` com a aplicação a funcionar.

## ☁️ Deploy no Streamlit Community Cloud

Para publicar a sua aplicação gratuitamente na internet:

1. Envie o seu código atualizado para o repositório principal no GitHub.
2. Aceda ao [Streamlit Community Cloud](https://share.streamlit.io/) e faça login.
3. Clique em **"New app"**, selecione este repositório, a *branch* principal e o arquivo `app.py`.
4. Antes de clicar em Deploy, aceda a **"Advanced settings"** (ou na aba **Secrets** após a criação) e cole o conteúdo do seu ficheiro `secrets.toml`.
5. Clique em **Deploy**.

## 📞 Autor

**Paulo Augusto Venelli Munhoz**
Profissional de Planejamento Comercial e Data Analytics.

* **Meu LinkedIn:** [https://www.linkedin.com/in/paulomunhoz/](https://www.linkedin.com/in/paulomunhoz/)
* **Meu GitHub:** [https://github.com/pauloavm](https://github.com/pauloavm)
* **Avaliação Gratuita de Seu LinkedIn:** [Formulário de Análise de Perfil](https://forms.gle/eqp8dADTU88bA39p6)