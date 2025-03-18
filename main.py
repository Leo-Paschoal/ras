import streamlit as st

# Define the pages
main_page = st.Page("home.py", title="Home")
page_2 = st.Page("page_2.py", title="Geral")
page_3 = st.Page("page_3.py", title="Perfil Profissional")

# Set up navigation
pg = st.navigation([main_page, page_2, page_3])

# Run the selected page
pg.run()