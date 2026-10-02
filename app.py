import streamlit as st
import plotly.graph_objects as go
import numpy as np
import requests
import re
import tempfile
import os
import unicodedata
from supabase import create_client, Client
from fpdf import FPDF

# Configuração da página
st.set_page_config(page_title="Perfil em Dados", layout="centered")

# --- GERENCIAMENTO DE ESTADO ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- FUNÇÕES DE VALIDAÇÃO E API ---
def is_valid_name(name):
    return re.match(r"^[A-Za-zÀ-ÿ\s]+$", name) is not None

def is_valid_email(email):
    return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email) is not None

def is_valid_linkedin(url):
    return "linkedin.com/in/" in url.lower()

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

@st.cache_data(ttl=3600)
def get_countries_and_states():
    try:
        r = requests.get("https://countriesnow.space/api/v0.1/countries/states", timeout=5)
        if r.status_code == 200:
            return r.json().get('data', [])
    except:
        pass
    return []

@st.cache_data(ttl=3600)
def get_cities(country, state):
    try:
        r = requests.post("https://countriesnow.space/api/v0.1/countries/state/cities", 
                          json={"country": country, "state": state}, timeout=5)
        if r.status_code == 200:
            return r.json().get('data', [])
    except:
        pass
    return []

# --- DADOS E DICIONÁRIOS ---
categories = [
    'MLOps', 'Pipelines de Dados', 'Banco de Dados', 'Visualização de Dados', 
    'Storytelling', 'Insights de Negócios', 'Experimentação', 'Estatística', 
    'Modelagem de ML', 'Implantação'
]

skill_descriptions = {
    'MLOps': 'Práticas para colocar e manter modelos em produção de forma confiável e escalável.',
    'Pipelines de Dados': 'Construção e automação de fluxos de extração, transformação e carregamento (ETL).',
    'Banco de Dados': 'Modelagem, gestão e consulta em bancos de dados relacionais e não-relacionais.',
    'Visualização de Dados': 'Criação de gráficos e dashboards para ilustrar dados complexos.',
    'Storytelling': 'Capacidade de comunicar descobertas de forma clara e persuasiva.',
    'Insights de Negócios': 'Compreensão do mercado para traduzir dados em ações estratégicas.',
    'Experimentação': 'Planejamento e execução de testes rigorosos (como Testes A/B).',
    'Estatística': 'Aplicação de métodos de probabilidade e inferência para garantir o rigor analítico.',
    'Modelagem de ML': 'Desenvolvimento, treinamento e ajuste de algoritmos preditivos.',
    'Implantação': 'Colocação de modelos ou aplicações no ar (deploy) em nuvem ou servidores.'
}

profiles = {
    'Engenheiro de Dados': [2, 5, 5, 2, 1, 1, 1, 1, 2, 4],
    'Engenheiro de ML': [5, 4, 3, 1, 1, 1, 3, 3, 5, 5],
    'Cientista de Dados': [2, 3, 3, 4, 4, 3, 5, 5, 5, 3],
    'Analista de Dados': [1, 2, 4, 5, 5, 5, 3, 3, 1, 1]
}

role_descriptions = {
    'Engenheiro de Dados': "Mestres em pipelines de dados, bancos de dados e implantação — mantendo o fluxo contínuo dos dados.",
    'Engenheiro de ML': "Focado em modelagem, experimentação e implantação de ML — trazendo o aprendizado de máquina à vida.",
    'Cientista de Dados': "Uma combinação de estatística, modelagem de ML e narrativa — transformando dados em insights acionáveis.",
    'Analista de Dados': "Especialistas em visualização de dados, narrativa e insights de negócios — tornando os dados compreensíveis e impactantes."
}

learning_resources = {
    'Engenheiro de Dados': {
        'Data Engineering Zoomcamp': 'https://github.com/DataTalksClub/data-engineering-zoomcamp',
        'Microsoft Learn - Azure Data Fundamentals': 'https://learn.microsoft.com/pt-br/training/azure/',
        'Documentacao Oficial do Apache Airflow': 'https://airflow.apache.org/docs/'
    },
    'Engenheiro de ML': {
        'Machine Learning Crash Course (Google)': 'https://developers.google.com/machine-learning/crash-course',
        'Fast.ai - Practical Deep Learning': 'https://course.fast.ai/',
        'MLOps Zoomcamp': 'https://github.com/DataTalksClub/mlops-zoomcamp'
    },
    'Cientista de Dados': {
        'Kaggle Micro-courses (Gratuitos e Praticos)': 'https://www.kaggle.com/learn',
        'CS229 Machine Learning (Stanford)': 'https://cs229.stanford.edu/',
        'Scikit-Learn Tutoriais e Exemplos': 'https://scikit-learn.org/stable/tutorial/index.html'
    },
    'Analista de Dados': {
        'Google Data Analytics (Auditavel no Coursera)': 'https://www.coursera.org/professional-certificates/google-data-analytics',
        'FreeCodeCamp - Data Analysis with Python': 'https://www.freecodecamp.org/learn/data-analysis-with-python/',
        'SQLZoo (Pratica Interativa de SQL)': 'https://sqlzoo.net/'
    }
}

# --- CLASSE PARA GERAR O PDF APRIMORADO ---
class PDFReport(FPDF):
    def footer(self):
        self.set_y(-25) 
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.set_y(-20)
        self.set_font("Arial", "I", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, remove_accents("Desenvolvido por Paulo Munhoz"), ln=True, align="C")
        self.set_text_color(0, 102, 204)
        self.set_font("Arial", "U", 9)
        self.cell(0, 5, "LinkedIn", link="https://www.linkedin.com/in/paulomunhoz/", align="C", ln=True)
        self.cell(0, 5, "GitHub", link="https://github.com/pauloavm", align="C", ln=True)

def generate_pdf(nome, resultado, descricao, recursos_dict, chart_path):
    pdf = PDFReport()
    pdf.add_page()
    
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 12, remove_accents("Relatório de Avaliação: Perfil em Dados"), ln=True, align="C")
    pdf.ln(5)
    
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.write(8, remove_accents(f"Olá, {nome}. Com base nas suas habilidades, o seu perfil tem forte alinhamento com: "))
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(41, 128, 185)
    pdf.write(8, remove_accents(f"{resultado}"))
    pdf.ln(12)
    
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 6, remove_accents(descricao.replace("—", "-")))
    pdf.ln(5)
    
    pdf.image(chart_path, x=45, w=120)
    pdf.ln(2)
    
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, remove_accents("Recursos Recomendados para Estudo (Clique para acessar):"), ln=True)
    
    pdf.set_font("Arial", "U", 11)
    pdf.set_text_color(0, 102, 204) 
    for curso, url in recursos_dict.items():
        pdf.set_font("Arial", "", 11)
        pdf.set_text_color(0, 0, 0)
        pdf.write(8, "  -  ")
        pdf.set_font("Arial", "U", 11)
        pdf.set_text_color(0, 102, 204)
        pdf.write(8, remove_accents(curso), link=url)
        pdf.ln(8)
        
    pdf.ln(8)
    
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(39, 174, 96) 
    pdf.set_text_color(255, 255, 255) 
    cta_text = remove_accents(" Quer se destacar? Clique aqui para uma Avaliação Gratuita do seu LinkedIn! ")
    pdf.cell(0, 12, cta_text, ln=True, align="C", fill=True, link="https://forms.gle/eqp8dADTU88bA39p6")
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name


# --- PÁGINA 1: HOME ---
def show_home():
    st.title("Descubra o seu lugar no Ecossistema de Dados")
    
    st.write("""
    O mercado de dados é vasto e repleto de especializações. Compreender onde as suas habilidades atuais se encaixam é o primeiro passo para direcionar os seus estudos e a sua carreira de forma estratégica.
    """)
    
    try:
        st.image("img/tipos_de_profissionais.jpg", use_container_width=True)
    except FileNotFoundError:
        st.warning("Imagem 'tipos_de_profissionais.jpg' não encontrada na pasta 'img/'.")

    st.markdown("### Conheça as Áreas de Atuação:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**🛠️ Engenheiro de Dados:**\n{role_descriptions['Engenheiro de Dados']}")
        st.markdown(f"**🤖 Engenheiro de ML:**\n{role_descriptions['Engenheiro de ML']}")
    with col2:
        st.markdown(f"**🔬 Cientista de Dados:**\n{role_descriptions['Cientista de Dados']}")
        st.markdown(f"**📊 Analista de Dados:**\n{role_descriptions['Analista de Dados']}")
        
    st.markdown("---")
    st.write("Pronto para descobrir qual destas áreas tem o maior *match* com o seu perfil atual?")
    
    if st.button("Iniciar o Quiz", type="primary"):
        navigate_to('quiz')


# --- PÁGINA 2: QUIZ ---
def show_quiz():
    rc = st.session_state.reset_counter # Variável que força a limpeza do formulário
    
    col1, col2 = st.columns([1, 8])
    with col1:
        if st.button("⬅ Voltar"):
            navigate_to('home')
            
    st.title("Quiz: Qual é o seu Perfil na Área de Dados?")
    st.info("🔒 **Privacidade:** Os dados não serão utilizados para fins comerciais. O objetivo é apenas registo e formar um grupo focado em vagas na área.")

    countries_data = get_countries_and_states()

    st.subheader("1. Informações Pessoais")
    
    c1, c2 = st.columns(2)
    with c1: nome = st.text_input("Nome*", key=f"nome_{rc}")
    with c2: sobrenome = st.text_input("Sobrenome", key=f"sobrenome_{rc}")

    c3, c4 = st.columns(2)
    pais = ""
    estado = ""
    state_names = []
    
    with c3:
        if countries_data:
            country_names = [item['name'] for item in countries_data]
            idx_brasil = country_names.index("Brazil") if "Brazil" in country_names else 0
            pais = st.selectbox("País", options=country_names, index=idx_brasil, key=f"pais_sel_{rc}")
            
            states_obj = next((item['states'] for item in countries_data if item['name'] == pais), [])
            state_names = [s['name'] for s in states_obj]
        else:
            pais = st.text_input("País", key=f"pais_txt_{rc}")

    with c4:
        if state_names:
            estado = st.selectbox("Estado / Província", options=state_names, key=f"est_sel_{rc}")
        else:
            estado = st.text_input("Estado / Província", key=f"est_txt_{rc}")

    c5, c6 = st.columns(2)
    cidade = ""
    with c5:
        if pais and estado and state_names:
            cities_data = get_cities(pais, estado)
            if cities_data:
                cidade = st.selectbox("Cidade", options=cities_data, key=f"cid_sel_{rc}")
            else:
                cidade = st.text_input("Cidade", key=f"cid_txt_{rc}")
        else:
            cidade = st.text_input("Cidade", key=f"cid_txt_fallback_{rc}")
            
    with c6: profissao = st.text_input("Profissão Atual", key=f"prof_{rc}")

    c7, c8 = st.columns(2)
    with c7: email = st.text_input("E-mail*", key=f"email_{rc}")
    with c8: linkedin = st.text_input("URL do LinkedIn", key=f"link_{rc}")

    st.markdown("---")
    st.subheader("2. Avaliação de Habilidades")
    st.write("Atribua uma nota de 1 (Iniciante) a 5 (Especialista).")
    
    user_scores = []
    c9, c10 = st.columns(2)
    
    for i, cat in enumerate(categories):
        col = c9 if i % 2 == 0 else c10
        with col:
            st.markdown(f"**{cat}**")
            st.caption(skill_descriptions[cat])
            score = st.slider(f"Nota para {cat}", min_value=1, max_value=5, value=3, label_visibility="collapsed", key=f"cat_{i}_{rc}")
            st.write("") 
        user_scores.append(score)
        
    if st.button("Descobrir meu perfil"):
        if not nome or not is_valid_name(nome):
            st.error("O campo 'Nome' é obrigatório e deve conter apenas letras e espaços.")
            st.stop()
        if not is_valid_email(email):
            st.error("Por favor, insira um e-mail válido.")
            st.stop()
        if linkedin and not is_valid_linkedin(linkedin):
            st.error("O link do LinkedIn parece estar incorreto. Ex: https://www.linkedin.com/in/seu-perfil")
            st.stop()

        distances = {}
        for role, scores in profiles.items():
            dist = np.linalg.norm(np.array(user_scores) - np.array(scores))
            distances[role] = dist
            
        best_match = min(distances, key=distances.get)
        
       # Mesclar o nome da categoria com a nota e separar por ponto e vírgula
        resultado_formatado = [f"{cat} {nota}" for cat, nota in zip(categories, user_scores)]
        scores_str = "; ".join(resultado_formatado)
        
        try:
            url = st.secrets["SUPABASE_URL"]
            key = st.secrets["SUPABASE_KEY"]
            supabase: Client = create_client(url, key)
            
            data = {
                "nome": nome,
                "sobrenome": sobrenome,
                "pais": pais,
                "estado": estado,
                "cidade": cidade,
                "profissao": profissao,
                "email": email,
                "linkedin": linkedin,
                "resultado": scores_str
            }
            supabase.table("quiz_results").insert(data).execute()
        except Exception as e:
            st.warning("Ocorreu um erro ao guardar os dados no Supabase. (Apenas exibindo o resultado)")
            st.error(f"Detalhe técnico: {e}")
            
        # Geração do Gráfico e PDF em memória para não perder os dados após clicar no botão de download
        cat_loop = categories + [categories[0]]
        user_loop = user_scores + [user_scores[0]]
        match_loop = profiles[best_match] + [profiles[best_match][0]]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=user_loop, theta=cat_loop, fill='toself', name='Você', line_color='rgba(136, 136, 136, 0.8)'))
        fig.add_trace(go.Scatterpolar(r=match_loop, theta=cat_loop, fill='toself', name=best_match, line_color='rgba(92, 157, 222, 0.8)'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=True, margin=dict(l=40, r=40, t=40, b=40))
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
            fig.write_image(tmp_img.name, width=600, height=500)
            chart_img_path = tmp_img.name
        
        pdf_path = generate_pdf(nome, best_match, role_descriptions[best_match], learning_resources[best_match], chart_img_path)
        
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
            
        os.remove(pdf_path)
        # os.remove(chart_img_path) # Comentado conforme solicitado - Não exclui o gráfico
        
        # Salva as informações da sessão para garantir que sobrevivem ao refresh da página
        st.session_state.best_match = best_match
        st.session_state.user_scores = user_scores
        st.session_state.nome_relatorio = nome
        st.session_state.pdf_bytes = pdf_bytes
        st.session_state.submitted_rc = rc

    # Renderização da Área de Resultado e Botões Finais
    if st.session_state.get('submitted_rc') == rc:
        best_match = st.session_state.best_match
        st.success(f"### O seu perfil ideal é: **{best_match}**")
        st.info(role_descriptions[best_match])

        # Recriar gráfico para a visualização na web
        cat_loop = categories + [categories[0]]
        user_loop = st.session_state.user_scores + [st.session_state.user_scores[0]]
        match_loop = profiles[best_match] + [profiles[best_match][0]]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=user_loop, theta=cat_loop, fill='toself', name='Você', line_color='rgba(136, 136, 136, 0.8)'))
        fig.add_trace(go.Scatterpolar(r=match_loop, theta=cat_loop, fill='toself', name=best_match, line_color='rgba(92, 157, 222, 0.8)'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=True, margin=dict(l=40, r=40, t=40, b=40))
        
        st.plotly_chart(fig, width='stretch')
        
        col_dl, col_reset = st.columns(2)
        with col_dl:
            st.download_button(
                label="📄 Baixar Relatório (PDF)",
                data=st.session_state.pdf_bytes,
                file_name=f"Resultado_Perfil_Dados_{st.session_state.nome_relatorio}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        with col_reset:
            if st.button("🔄 Limpar e Refazer o Teste", type="primary", use_container_width=True):
                st.session_state.reset_counter += 1
                st.rerun()

# --- CONTROLE DE FLUXO PRINCIPAL ---
if __name__ == "__main__":
    if st.session_state.page == 'home':
        show_home()
    elif st.session_state.page == 'quiz':
        show_quiz()