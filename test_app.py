import streamlit as st

st.title("Test App")
st.write("If you can see this, Streamlit is working!")

uploaded_file = st.file_uploader("Test uploader", type=["txt", "pdf"])

if uploaded_file:
    st.success(f"File uploaded: {uploaded_file.name}")

st.write("End of test app")