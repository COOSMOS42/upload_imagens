import streamlit as st
import cloudinary
import cloudinary.uploader
import cloudinary.api
import tempfile

# CONFIGURAÇÃO
cloudinary.config(
    cloud_name=st.secrets["cloudinary"]["cloud_name"],
    api_key=st.secrets["cloudinary"]["api_key"],
    api_secret=st.secrets["cloudinary"]["api_secret"]
)

# Inicializa o estado anterior do curso
if 'selected_course' not in st.session_state:
    st.session_state.selected_course = None

st.title("Faça o Upload das Imagens")

# Seleção do curso
cursos = st.selectbox(
    'Escolha o Curso',
    ('Curso Básico de Eletricidade', 'Curso de Design de Sobrancelhas', 'Curso de Manicure e Pedicure')
)

# Se o curso mudou, limpa o uploader
if cursos != st.session_state.selected_course:
    st.session_state.selected_course = cursos
    st.session_state['uploaded_files'] = []  # Limpa as imagens salvas

# Uploader controlado por session_state
uploaded_files = st.file_uploader(
    "Envie sua imagem",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True,
    key=f"uploader_{cursos}"  # força a recriação quando o curso muda
)

if uploaded_files:
    urls = []
    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            temp_path = temp_file.name

        with st.spinner(f"Enviando {uploaded_file.name}..."):
            result = cloudinary.uploader.upload(
                temp_path,
                folder=cursos
            )
            urls.append(result['secure_url'])

    st.success("Imagens enviadas com sucesso!")


