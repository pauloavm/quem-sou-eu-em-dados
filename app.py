import streamlit as st
import plotly.graph_objects as go
import numpy as np
from supabase import create_client, Client
from fpdf import FPDF
import tempfile
import os

# Configuração da página
st.set_page_config(page_title="Quiz: Seu Perfil de Dados", layout="centered")

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

# Recursos gratuitos para aprimoramento
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
        # Substitua o link abaixo pela sua URL exata caso necessário
        self.cell(0, 10, "Conecte-se com o criador no LinkedIn: linkedin.com/in/paulo-augusto-venelli-munhoz", 0, 0, "C")

def generate_pdf(nome, resultado, descricao, recursos):
    pdf = PDFReport()
    pdf.add_page()
    
    # Título
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatório de Perfil: Profissional de Dados", ln=True, align="C")
    pdf.ln(10)
    
    # Saudação e Resultado
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Olá, {nome}.", ln=True)
    pdf.cell(0, 10, f"O seu perfil ideal calculado e: {resultado}", ln=True)
    pdf.ln(5)
    
    # Descrição do Cargo
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Sobre a sua area de atuacao:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, descricao.replace("—", "-"))
    pdf.ln(10)
    
    # Recursos para Aprimoramento
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Onde aprimorar os seus conhecimentos gratuitamente:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, recursos)
    
    # Salvar em ficheiro temporário
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

# --- APLICAÇÃO PRINCIPAL ---
def main():
    st.title("Quiz: Qual é o seu Perfil na Área de Dados?")
    
    # Aviso de Privacidade
    st.info("🔒 **Privacidade dos Dados:** As informações recolhidas não serão utilizadas para fins comerciais. O objetivo é apenas registo e a formação de um futuro grupo focado em vagas na área de dados.")

    # Formulário unificado
    with st.form("quiz_form"):
        st.subheader("1. Informações Pessoais")
        
        c1, c2 = st.columns(2)
        with c1:
            nome = st.text_input("Nome")
            pais = st.text_input("País")
            cidade = st.text_input("Cidade")
            email = st.text_input("E-mail")
        with c2:
            sobrenome = st.text_input("Sobrenome")
            estado = st.text_input("Estado")
            profissao = st.text_input("Profissão Atual")
            linkedin = st.text_input("URL do LinkedIn")

        st.markdown("---")
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
            
        submitted = st.form_submit_button("Descobrir meu perfil")

    if submitted:
        # Validação simples
        if not nome or not email:
            st.error("Por favor, preencha pelo menos o Nome e o E-mail.")
            return

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
                "nome": nome,
                "sobrenome": sobrenome,
                "pais": pais,
                "estado": estado,
                "cidade": cidade,
                "profissao": profissao,
                "email": email,
                "linkedin": linkedin,
                "resultado": best_match
            }
            supabase.table("quiz_results").insert(data).execute()
        except Exception as e:
            st.warning("Ocorreu um erro ao guardar os dados no Supabase. Verifique as credenciais.")
            st.write(e)
            
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
        st.plotly_chart(fig, use_container_width=True)
        
        # Gerar e disponibilizar o PDF
        pdf_path = generate_pdf(nome, best_match, role_descriptions[best_match], learning_resources[best_match])
        
        with open(pdf_path, "rb") as file:
            st.download_button(
                label="📄 Baixar Relatório (PDF)",
                data=file,
                file_name=f"Resultado_Perfil_Dados_{nome}.pdf",
                mime="application/pdf"
            )
            
        # Remover o ficheiro temporário após carregar para a memória
        os.remove(pdf_path)

if __name__ == "__main__":
    main()