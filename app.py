import streamlit as st
import utils

st.title("Validate Copy")

formularioPrincipal = st.form("validateCopy")

@st.dialog("Seus resultados:")
def resultados(copy):
    st.write(utils.CreateTokens(copy))

async def spinLoader(func):
    while await func:
        st.spinner('Carregando resultados')

with formularioPrincipal:
    product = st.selectbox("Selecione um produto para qual a copy é destinada", ("Teste1", "Teste2", "Teste3"))
    copy = st.text_area("Insira a copy que você deseja avaliar")
    submit = st.form_submit_button("Enviar")
    if submit:
        if copy:
            resultados(copy)



