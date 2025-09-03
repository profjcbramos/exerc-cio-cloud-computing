import streamlit as st

# Estudando colunas
# Estudando containers
sb = st.sidebar

with sb:
    

col1, col2, col3 = st.columns((2,1,1))

with col1:
    col1.markdown('João')
    with st.container(border=True):
        st.text("Tank")
        st.image("data/Tank.png", width=200)

with col2:
    col2.markdown('Luís')
    with st.container(border=True):
        st.text("Marduk")

with col3:
    col3.markdown('Marcos')
    with st.container(border=True):
        st.text("Risonho")



