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

    # Perfis de referência (notas de 1 a 5)
    profiles = {
        'Engenheiro de Dados': [2, 5, 5, 2, 1, 1, 1, 1, 2, 4],
        'Engenheiro de ML': [5, 4, 3, 1, 1, 1, 3, 3, 5, 5],
        'Cientista de Dados': [2, 3, 3, 4, 4, 3, 5, 5, 5, 3],
        'Analista de Dados': [1, 2, 4, 5, 5, 5, 3, 3, 1, 1]
    }

    # Descrições de cada perfil fornecidas
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
            if i % 2 == 0:
                with col1:
                    score = st.slider(cat, min_value=1, max_value=5, value=3)
            else:
                with col2:
                    score = st.slider(cat, min_value=1, max_value=5, value=3)
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
        
        # Exibição dos resultados e da explicação
        st.success(f"### O seu perfil ideal é: **{best_match}**")
        st.info(role_descriptions[best_match])
        
        st.write("Abaixo está a comparação visual entre as suas habilidades e o perfil recomendado.")

        # Preparar dados para o gráfico de radar (fechar o ciclo)
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