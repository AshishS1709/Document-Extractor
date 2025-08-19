import streamlit as st
import io
import json
from utils.pdf_utils import extract_text_from_pdf
from extractor import classify_doc, extract_fields

# Streamlit UI
st.set_page_config(page_title="Agentic Document Extraction", page_icon="📄", layout="wide")
st.title("📄 Agentic Document Extraction")
st.write("Upload a document (PDF, Image, or Text) to extract structured information")

# File uploader
uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.success(f"Uploaded file: {uploaded_file.name}")

    content = None
    doc_type = None

    try:
        # If it's a PDF
        if uploaded_file.type == "application/pdf":
            with st.spinner("Extracting text from PDF..."):
                content = extract_text_from_pdf(uploaded_file)
            
            st.write(f"✅ Successfully extracted text from PDF ({len(content)} characters)")
            
            # Show preview of extracted text
            st.subheader("📄 Text Preview")
            preview_text = content[:1000] + "..." if len(content) > 1000 else content
            st.text_area("Extracted Text Preview", preview_text, height=200, disabled=True)

        # If it's a text file
        elif uploaded_file.type == "text/plain":
            content = uploaded_file.read().decode("utf-8")
            st.subheader("📄 Extracted Text")
            preview_text = content[:1000] + "..." if len(content) > 1000 else content
            st.text_area("Text Content", preview_text, height=200, disabled=True)

        # If it's an image
        elif uploaded_file.type in ["image/png", "image/jpeg"]:
            st.image(uploaded_file, caption="Uploaded Image")
            st.warning("Image OCR not implemented yet. Please use PDF or text files.")
            content = None

        # Process the extracted content
        if content and content.strip():
            
            # Step 1: Classify document
            with st.spinner("Classifying document..."):
                doc_type = classify_doc(content)
            
            st.subheader("📋 Document Classification")
            st.info(f"Document Type: **{doc_type.upper()}**")
            
            # Step 2: Extract fields based on document type
            with st.spinner("Extracting structured information..."):
                # Define fields based on document type
                field_mapping = {
                    'invoice': ['Invoice Number', 'Date', 'Vendor Name', 'Total Amount', 'Tax Amount'],
                    'medical_bill': ['Patient Name', 'Bill Date', 'Hospital Name', 'Total Amount', 'Insurance'],
                    'prescription': ['Patient Name', 'Doctor Name', 'Prescription Date', 'Medications'],
                    'other': ['Date', 'Amount', 'Key Information']
                }
                
                fields_to_extract = field_mapping.get(doc_type, field_mapping['other'])
                extracted_info = extract_fields(content, doc_type, fields_to_extract)
            
            # Display results
            st.subheader("📊 Extracted Information")
            
            # Try to parse as JSON for better display
            try:
                if extracted_info.strip().startswith('{'):
                    parsed_data = json.loads(extracted_info)
                    st.json(parsed_data)
                else:
                    st.markdown("**Extracted Data:**")
                    st.write(extracted_info)
            except json.JSONDecodeError:
                st.markdown("**Extracted Data:**")
                st.write(extracted_info)
            
            # Download option
            st.download_button(
                label="📥 Download Extracted Data",
                data=extracted_info,
                file_name=f"extracted_{doc_type}_{uploaded_file.name}.json",
                mime="application/json"
            )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Make sure your GROQ_API_KEY is set and all dependencies are installed.")

# Sidebar with information
with st.sidebar:
    st.header("📋 Instructions")
    st.markdown("""
    1. **Upload** a document (PDF or text file)
    2. **Wait** for text extraction and classification
    3. **Review** the extracted structured data
    4. **Download** the results
    
    **Supported Document Types:**
    - 📄 Invoice
    - 🏥 Medical Bill  
    - 💊 Prescription
    - 📝 Other documents
    """)
    
    st.header("⚙️ Setup")
    st.markdown("""
    **Required:**
    - GROQ API Key (set as environment variable)
    - Python packages: `streamlit`, `pdfplumber`, `groq`
    
    **Set API Key:**
    ```bash
    export GROQ_API_KEY="your_key_here"
    ```
    """)
    
    # API Key status check
    import os
    if os.getenv("GROQ_API_KEY"):
        st.success("✅ GROQ_API_KEY is set")
    else:
        st.error("❌ GROQ_API_KEY not found")