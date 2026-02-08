import streamlit as st
from PIL import Image
import io
import zipfile
from datetime import datetime
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Product Factory Pro", layout="wide", initial_sidebar_state="expanded")

# --- CLEAN MIDNIGHT GRAPHITE UI ---
st.markdown("""
    <style>
        .stApp { background-color: #0B0E14; color: #E6edf3; }
        [data-testid="stSidebar"] { background-color: #161B22; border-right: 1px solid #30363D; }
        h1, h2, h3, h4, label, .stWidgetLabel p { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
        
        /* Input Styling */
        .stTextInput input, .stSelectbox div, .stTextArea textarea, .stNumberInput input {
            background-color: #0D1117 !important; color: #FFFFFF !important;
            border: 1px solid #30363D !important; border-radius: 6px !important;
        }

        /* BUTTONS: Electric Blue with BLACK text */
        .stButton>button {
            width: 100%; border-radius: 6px; border: none;
            background-color: #58A6FF !important; color: #000000 !important;
            font-weight: 700 !important; cursor: pointer !important;
        }
        .stButton>button:hover { background-color: #FFFFFF !important; }

        /* Download Button Specific Styling */
        .stDownloadButton>button {
            background-color: #238636 !important; color: #FFFFFF !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: PROMPT GENERATOR ---
st.sidebar.title("🤖 AI Prompt Studio")
currency = st.sidebar.selectbox("Currency", ["PKR", "USD", "AED", "GBP", "EUR"])
category = st.sidebar.selectbox("Category", ["Clothing", "Shoes", "Jewelry", "Stationery", "Paper Soap"])

if category == "Clothing":
    fabric_choice = st.sidebar.selectbox("Fabric", ["Cotton", "Lawn", "Silk", "Linen", "Chiffon", "Other"])
    attr1 = st.sidebar.text_input("Manual Fabric") if fabric_choice == "Other" else fabric_choice
    attr2 = st.sidebar.selectbox("Age Group", ["Newly Born", "Child", "Teenage", "Adult"])
    # NEW: Selection Button for Size Chart
    need_size_chart = st.sidebar.checkbox("Include Size Chart?", value=True)
else:
    need_size_chart = False
    attr1 = st.sidebar.text_input("Material/Attribute 1")
    attr2 = st.sidebar.text_input("Spec/Attribute 2")

prod_name = st.sidebar.text_input("Product Name", "Classic Collection")
focus_kw = st.sidebar.text_input("Focus Keyword", "premium quality")
extra_details = st.sidebar.text_area("Extra Details")

st.sidebar.divider()
generate_btn = st.sidebar.button("✨ GENERATE AI PROMPT")

# --- MAIN AREA ---
st.title("🚀 Product Content Factory")
tab1, tab2, tab3 = st.tabs(["📸 IMAGE CONVERTER", "📈 PROFIT CALCULATOR", "♊ AI PROMPT HUB"])

# --- TAB 1: IMAGE CONVERTER ---
with tab1:
    st.subheader("WordPress Optimized WebP Converter")
    target_size = st.selectbox("Export Size (Pixels)", [800, 1000, 1200], index=1)
    uploaded_files = st.file_uploader("Upload Photos", type=['jpg', 'png', 'webp'], accept_multiple_files=True)
    if uploaded_files:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for uploaded_file in uploaded_files:
                img = Image.open(uploaded_file).convert("RGB")
                new_img = Image.new("RGB", (target_size, target_size), (255, 255, 255))
                img.thumbnail((target_size, target_size))
                offset = ((target_size-img.size[0])//2, (target_size-img.size[1])//2)
                new_img.paste(img, offset)
                img_io = io.BytesIO()
                new_img.save(img_io, "WEBP", quality=75)
                zip_file.writestr(f"{uploaded_file.name.split('.')[0]}.webp", img_io.getvalue())
        st.download_button("📦 DOWNLOAD IMAGES (ZIP)", zip_buffer.getvalue(), "images.zip")

# --- TAB 2: PROFIT CALCULATOR & SIZE CHART ---
with tab2:
    st.subheader("Profit Breakdown")
    c1, c2 = st.columns(2)
    cost_p = c1.number_input(f"Cost Price", min_value=0.0)
    sell_p = c2.number_input(f"Selling Price", min_value=0.0)
    
    net_profit = sell_p - cost_p
    st.metric("Net Profit", f"{currency} {net_profit:,.2f}")

    if need_size_chart:
        st.divider()
        st.subheader("📏 Product Size Chart")
        
        # Table Data
        size_data = {
            "Size": ["XS", "S", "M", "L", "XL", "XXL"],
            "Chest (Inches)": ["34", "36", "38", "40", "44", "48"],
            "Waist (Inches)": ["28", "30", "32", "34", "38", "42"],
            "Length (Inches)": ["27", "28", "29", "30", "31", "32"]
        }
        df = pd.DataFrame(size_data)
        
        # Display as Interactive Table (Copyable)
        st.dataframe(df, use_container_width=True)
        
        # Download as CSV (For Word/Excel)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Size Chart (CSV)", data=csv, file_name="size_chart.csv", mime="text/csv")
        st.caption("Tip: Select and copy the table above directly, or download the CSV to import into Word/Excel.")

# --- TAB 3: AI PROMPT HUB ---
with tab3:
    if generate_btn:
        st.code(f"Product: {prod_name}\nKeyword: {focus_kw}\nDetails: {extra_details}", language="markdown")
