import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Configuração da página
st.set_page_config(page_title="Quiz: Seu Perfil de Dados", layout="centered")

def main():
    st.title("Quiz: Qual é o seu Perfil na Área de Dados?")
    st.write("""
    Avalie o seu nível de habilidade ou interesse em cada uma das áreas abaixo, 
    atribuindo uma nota de 1 (Muito Baixo/Iniciante) a 5 (Muito Alto/Especialista).
    O sistema irá recomendar a área de atuação que melhor se alinha ao seu perfil.
    """)

    # Categorias baseadas no gráfico
    categories = [
        'MLOps', 'Pipelines de Dados', 'Banco de Dados', 'Visualização de Dados', 
        'Storytelling', 'Insights de Negócios', 'Experimentação', 'Estatística', 
        'Modelagem de ML', 'Implantação'
    ]
    
    # Explicação de cada habilidade
    skill_descriptions = {
        'MLOps': 'Práticas para colocar e manter modelos de Machine Learning em produção de forma confiável e escalável.',
        'Pipelines de Dados': 'Construção e automação de fluxos de extração, transformação e carregamento (ETL) de dados.',
        'Banco de Dados': 'Modelagem, gestão e consulta (como SQL) em bancos de dados relacionais e não-relacionais.',
        'Visualização de Dados': 'Criação de gráficos e dashboards (ex: Power BI, Tableau) para ilustrar dados complexos.',
        'Storytelling': 'Capacidade de comunicar descobertas de forma clara, construindo uma narrativa persuasiva.',
        'Insights de Negócios': 'Compreensão do mercado para traduzir resultados de dados em ações estratégicas para a empresa.',
        'Experimentação': 'Planejamento e execução de testes (como Testes A/B) para validar hipóteses de forma rigorosa.',
        'Estatística': 'Aplicação de métodos de probabilidade, inferência e análise matemática para garantir o rigor dos dados.',
        'Modelagem de ML': 'Desenvolvimento, treinamento e ajuste de algoritmos preditivos e aprendizado de máquina.',
        'Implantação': 'Colocação de modelos, scripts ou aplicações no ar (deploy) em servidores ou serviços de nuvem.'
    }

    # Perfis de referência (notas de 1 a 5)
    profiles = {
        'Engenheiro de Dados': [2, 5, 5, 2, 1, 1, 1, 1, 2, 4],
        'Engenheiro de ML': [5, 4, 3, 1, 1, 1, 3, 3, 5, 5],
        'Cientista de Dados': [2, 3, 3, 4, 4, 3, 5, 5, 5, 3],
        'Analista de Dados': [1, 2, 4, 5, 5, 5, 3, 3, 1, 1]
    }

    # Descrições de cada perfil
    role_descriptions = {
        'Engenheiro de Dados': "Mestres em pipelines de dados, bancos de dados e implantação — mantendo o fluxo contínuo dos dados.",
        'Engenheiro de ML': "Focado em modelagem, experimentação e implantação de ML — trazendo o aprendizado de máquina à vida.",
        'Cientista de Dados': "Uma combinação de estatística, modelagem de ML e narrativa — transformando dados em insights acionáveis.",
        'Analista de Dados': "Especialistas em visualização de dados, narrativa e insights de negócios — tornando os dados compreensíveis e impactantes."
    }

    # Formulário para o preenchimento
    user_scores = []
    with st.form("quiz_form"):
        st.subheader("Suas Habilidades")
        
        col1, col2 = st.columns(2)
        
        for i, cat in enumerate(categories):
            col = col1 if i % 2 == 0 else col2
            
            with col:
                # 1. Habilidade (em negrito)
                st.markdown(f"**{cat}**")
                
                # 2. Explicação (em texto menor/cinza)
                st.caption(skill_descriptions[cat])
                
                # 3. Régua (com o título padrão oculto para manter a ordem solicitada)
                score = st.slider(
                    f"Nota para {cat}", 
                    min_value=1, 
                    max_value=5, 
                    value=3, 
                    label_visibility="collapsed"
                )
                
                st.write("") # Espaçamento para o próximo item
                
            user_scores.append(score)
            
        submitted = st.form_submit_button("Descobrir meu perfil")

    if submitted:
        # Calcular a similaridade (distância euclidiana)
        distances = {}
        for role, scores in profiles.items():
            dist = np.linalg.norm(np.array(user_scores) - np.array(scores))
            distances[role] = dist
            
        # Determinar o perfil com a menor distância
        best_match = min(distances, key=distances.get)
        
        st.success(f"### O seu perfil ideal é: **{best_match}**")
        st.info(role_descriptions[best_match])
        
        st.write("Abaixo está a comparação visual entre as suas habilidades e o perfil recomendado.")

        # Preparar dados para o gráfico de radar
        cat_loop = categories + [categories[0]]
        user_loop = user_scores + [user_scores[0]]
        match_loop = profiles[best_match] + [profiles[best_match][0]]

        # Criar o gráfico de radar
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=user_loop,
            theta=cat_loop,
            fill='toself',
            name='Você',
            line_color='rgba(136, 136, 136, 0.8)'
        ))

        fig.add_trace(go.Scatterpolar(
            r=match_loop,
            theta=cat_loop,
            fill='toself',
            name=best_match,
            line_color='rgba(92, 157, 222, 0.8)'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5])
            ),
            showlegend=True,
            margin=dict(l=40, r=40, t=40, b=40)
        )

        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()