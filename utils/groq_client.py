import os
from groq import Groq
import streamlit as st

_groq_client = None

def get_groq_client():
    global _groq_client
    if _groq_client is None:
        api_key = (
            st.secrets.get("GROQ_API_KEY")
            if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets
            else os.getenv("GROQ_API_KEY")
        )
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not set. Add to Streamlit Secrets or environment.")
        _groq_client = Groq(api_key=api_key)
    return _groq_client
