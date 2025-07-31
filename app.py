import streamlit as st
import tempfile
import os
from extractor import extract_invoice_data
from utils import save_to_csv

st.set_page_config(page_title="Invoice Extractor", layout="centered")

st.title("📄 Invoice Data Extractor")
st.markdown("Upload your invoice image (JPG/PNG), and extract key fields + full OCR text.")

uploaded_file = st.file_uploader("Upload Invoice Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.image(tmp_path, caption="Uploaded Invoice", use_column_width=True)
    st.info("🔍 Extracting data...")

    result = extract_invoice_data(tmp_path)

    if "Error" in result:
        st.error(result["Error"])
    else:
        st.success("✅ Data Extracted")
        for key, value in result.items():
            st.write(f"**{key}**: {value}")

        save_to_csv(result)
        st.success("📁 Data saved to `extracted_invoices.csv`")

        if st.checkbox("Show Raw OCR Text"):
            st.text_area("Full OCR Text", result["Full Text"], height=250)

    # Clean up temp file
    os.remove(tmp_path)
