import streamlit as st
import plotly.graph_objects as go
import numpy as np
from supabase import create_client, Client
from fpdf import FPDF
import tempfile
import os
import re
import requests

# Configuração da página
st.set_page_config(page_title="Quiz: Seu Perfil de Dados", layout="centered")

# --- FUNÇÕES DE VALIDAÇÃO ---
def is_valid_text(text):
    # Permite letras, espaços e acentos. Rejeita números avulsos ou símbolos absurdos. Mínimo 2 caracteres.
    if not text: return False
    return bool(re.match(r"^[A-Za-zÀ-ÿ\s]{2,}$", text.strip()))

def is_valid_email(email):
    if not email: return False
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email.strip()))

def is_valid_linkedin(url):
    if not url: return False
    return bool(re.match(r"^(https?:\/\/)?([\w]+\.)?linkedin\.com\/.*$", url.strip()))

# --- FUNÇÕES DE BUSCA DE LOCALIZAÇÃO (COM CACHE PARA NÃO FICAR LENTO) ---
@st.cache_data(ttl=86400) # Cache de 1 dia
def get_countries():
    try:
        r = requests.get("https://countriesnow.space/api/v0.1/countries")
        if r.status_code == 200:
            return sorted([country['country'] for country in r.json()['data']])
    except:
        pass
    return ["Brasil", "Portugal", "Estados Unidos"] # Fallback básico

@st.cache_data(ttl=86400)
def get_states(country):
    try:
        r = requests.post("https://countriesnow.space/api/v0.1/countries/states", json={"country": country})
        if r.status_code == 200:
            return sorted([state['name'] for state in r.json()['data']['states']])
    except:
        pass
    return []

@st.cache_data(ttl=86400)
def get_cities(country, state):
    try:
        r = requests.post("https://countriesnow.space/api/v0.1/countries/state/cities", json={"country": country, "state": state})
        if r.status_code == 200:
            return sorted(r.json()['data'])
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
    'Engenheiro de Dados': "Cursos gratuitos em: Data Engineering Zoomcamp (DataTalks.Club), Microsoft Learn (Azure Data), e tutoriais de Apache Airflow/Spark no YouTube.",
    'Engenheiro de ML': "Cursos gratuitos em: Machine Learning Crash Course (Google), Fast.ai (Practical Deep Learning), e MLOps Zoomcamp.",
    'Cientista de Dados': "Cursos gratuitos em: Kaggle Micro-courses, CS229 (Stanford/YouTube), e documentação do Scikit-Learn.",
    'Analista de Dados': "Cursos gratuitos em: Google Data Analytics (auditoria no Coursera), FreeCodeCamp (Data Analysis with Python), e SQLZoo."
}

# --- FUNÇÃO PARA GERAR PDF ---
class PDFReport(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, "Conecte-se com o criador no LinkedIn: linkedin.com/in/paulo-augusto-venelli-munhoz", 0, 0, "C")

def generate_pdf(nome, resultado, descricao, recursos):
    pdf = PDFReport()
    pdf.add_page()
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatorio de Perfil: Profissional de Dados", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Ola, {nome}.", ln=True)
    pdf.cell(0, 10, f"O seu perfil ideal calculado e: {resultado}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Sobre a sua area de atuacao:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, descricao.replace("—", "-"))
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Onde aprimorar os seus conhecimentos gratuitamente:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, recursos)
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

# --- APLICAÇÃO PRINCIPAL ---
def main():
    st.title("Quiz: Qual é o seu Perfil na Área de Dados?")
    st.info("🔒 **Privacidade dos Dados:** As informações recolhidas não serão utilizadas para fins comerciais. O objetivo é apenas registo e a formação de um futuro grupo focado em vagas na área de dados.")

    # 1. Informações Pessoais (Sem st.form para permitir atualização dinâmica dos selects)
    st.subheader("1. Informações Pessoais")
    
    c1, c2 = st.columns(2)
    with c1:
        nome = st.text_input("Nome*")
        email = st.text_input("E-mail*")
        profissao = st.text_input("Profissão Atual*")
    with c2:
        sobrenome = st.text_input("Sobrenome*")
        linkedin = st.text_input("URL do LinkedIn*")
    
    st.markdown("**Localização**")
    c_loc1, c_loc2, c_loc3 = st.columns(3)
    
    # Lógica em cascata para País -> Estado -> Cidade
    with c_loc1:
        paises_lista = [""] + get_countries()
        pais = st.selectbox("País*", options=paises_lista)
    
    estado = ""
    cidade = ""
    with c_loc2:
        if pais:
            estados_lista = get_states(pais)
            if estados_lista:
                estado = st.selectbox("Estado/Província*", options=[""] + estados_lista)
            else:
                estado = st.text_input("Estado/Província*") # Fallback se API falhar ou não tiver estados
        else:
            st.selectbox("Estado/Província*", options=["Selecione o País primeiro"], disabled=True)
            
    with c_loc3:
        if estado and pais:
            cidades_lista = get_cities(pais, estado)
            if cidades_lista:
                cidade = st.selectbox("Cidade*", options=[""] + cidades_lista)
            else:
                cidade = st.text_input("Cidade*") # Fallback se API falhar ou não tiver cidades
        else:
             st.selectbox("Cidade*", options=["Selecione o Estado primeiro"], disabled=True)

    st.markdown("---")
    
    # 2. Avaliação de Habilidades
    st.subheader("2. Avaliação de Habilidades")
    st.write("Atribua uma nota de 1 (Iniciante) a 5 (Especialista).")
    
    user_scores = []
    c3, c4 = st.columns(2)
    
    for i, cat in enumerate(categories):
        col = c3 if i % 2 == 0 else c4
        with col:
            st.markdown(f"**{cat}**")
            st.caption(skill_descriptions[cat])
            score = st.slider(f"Nota para {cat}", min_value=1, max_value=5, value=3, label_visibility="collapsed")
            st.write("") 
        user_scores.append(score)
        
    # O botão de envio fica fora do form
    if st.button("Descobrir meu perfil", type="primary"):
        # Validação Robusta
        erros = []
        if not is_valid_text(nome): erros.append("O 'Nome' inserido é inválido ou muito curto.")
        if not is_valid_text(sobrenome): erros.append("O 'Sobrenome' inserido é inválido.")
        if not is_valid_text(profissao): erros.append("A 'Profissão' inserida contém caracteres inválidos.")
        if not is_valid_email(email): erros.append("O formato do 'E-mail' é inválido.")
        if not is_valid_linkedin(linkedin): erros.append("O link do 'LinkedIn' é inválido (deve conter linkedin.com).")
        if not pais: erros.append("Selecione um País.")
        if not estado or estado == "Selecione o País primeiro": erros.append("Informe o Estado.")
        if not cidade or cidade == "Selecione o Estado primeiro": erros.append("Informe a Cidade.")

        if erros:
            st.error("Corrija os seguintes erros antes de continuar:")
            for erro in erros:
                st.warning(erro)
        else:
            # Calcular Perfil
            distances = {}
            for role, scores in profiles.items():
                dist = np.linalg.norm(np.array(user_scores) - np.array(scores))
                distances[role] = dist
                
            best_match = min(distances, key=distances.get)
            
            # Enviar para o Supabase
            try:
                url = st.secrets["SUPABASE_URL"]
                key = st.secrets["SUPABASE_KEY"]
                supabase: Client = create_client(url, key)
                
                data = {
                    "nome": nome.strip(),
                    "sobrenome": sobrenome.strip(),
                    "pais": pais,
                    "estado": estado,
                    "cidade": cidade,
                    "profissao": profissao.strip(),
                    "email": email.strip(),
                    "linkedin": linkedin.strip(),
                    "resultado": best_match
                }
                supabase.table("quiz_results").insert(data).execute()
            except Exception as e:
                st.warning("Ocorreu um erro ao guardar os dados no Supabase. (Apenas exibindo o resultado)")
                st.error(f"Detalhe técnico do erro: {e}")  # Isto vai imprimir o erro exato na tela em vermelho
            # Apresentação do Resultado
            st.success(f"### O seu perfil ideal é: **{best_match}**")
            st.info(role_descriptions[best_match])
            
            st.write("Abaixo está a comparação visual entre as suas habilidades e o perfil recomendado.")

            cat_loop = categories + [categories[0]]
            user_loop = user_scores + [user_scores[0]]
            match_loop = profiles[best_match] + [profiles[best_match][0]]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=user_loop, theta=cat_loop, fill='toself', name='Você', line_color='rgba(136, 136, 136, 0.8)'))
            fig.add_trace(go.Scatterpolar(r=match_loop, theta=cat_loop, fill='toself', name=best_match, line_color='rgba(92, 157, 222, 0.8)'))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=True, margin=dict(l=40, r=40, t=40, b=40))
            st.plotly_chart(fig, width='stretch')
            
            # Gerar e disponibilizar o PDF
            pdf_path = generate_pdf(nome, best_match, role_descriptions[best_match], learning_resources[best_match])
            
            with open(pdf_path, "rb") as file:
                st.download_button(
                    label="📄 Baixar Relatório (PDF)",
                    data=file,
                    file_name=f"Resultado_Perfil_Dados_{nome}.pdf",
                    mime="application/pdf"
                )
                
            os.remove(pdf_path)

if __name__ == "__main__":
    main()