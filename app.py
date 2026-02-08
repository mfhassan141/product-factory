import streamlit as st
from PIL import Image
import io
import zipfile
from datetime import datetime
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Product Factory Pro", layout="wide", initial_sidebar_state="expanded")

# --- UI STYLING ---
st.markdown("""
    <style>
        .stApp { background-color: #0B0E14; color: #E6edf3; }
        [data-testid="stSidebar"] { background-color: #161B22; border-right: 1px solid #30363D; }
        h1, h2, h3, h4, label, .stWidgetLabel p { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
        
        .stTextInput input, .stSelectbox div, .stTextArea textarea, .stNumberInput input {
            background-color: #0D1117 !important; color: #FFFFFF !important;
            border: 1px solid #30363D !important; border-radius: 6px !important;
        }

        .stButton>button {
            width: 100%; border-radius: 6px; border: none;
            background-color: #58A6FF !important; color: #000000 !important;
            font-weight: 700 !important; cursor: pointer !important;
        }
        .stButton>button:hover { background-color: #FFFFFF !important; }

        .stDownloadButton>button {
            background-color: #238636 !important; color: #FFFFFF !important;
            cursor: pointer !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: PROMPT GENERATOR ---
st.sidebar.title("🤖 AI Prompt Studio")
currency = st.sidebar.selectbox("Currency", ["PKR", "USD", "AED", "GBP", "EUR"])
category = st.sidebar.selectbox("Category", ["Clothing", "Shoes", "Jewelry", "Stationery", "Paper Soap"])

attr1, attr2, gender = "", "", ""

# --- RESTORED CATEGORY LOGIC ---
if category == "Clothing":
    gender = st.sidebar.radio("Target Gender", ["Male", "Female", "Unisex"])
    fabric_choice = st.sidebar.selectbox("Fabric", ["Cotton", "Lawn", "Silk", "Linen", "Chiffon", "Jersey", "Wool", "Other"])
    attr1 = st.sidebar.text_input("Manual Fabric") if fabric_choice == "Other" else fabric_choice
    attr2 = st.sidebar.selectbox("Age Group", ["Newly Born", "Child", "Teenage", "Adult"])
    need_size_chart = st.sidebar.checkbox("Include Size Chart?", value=True)

elif category == "Shoes":
    gender = st.sidebar.radio("Target Gender", ["Male", "Female", "Unisex"])
    attr1 = st.sidebar.text_input("Material", "Leather")
    attr2 = st.sidebar.text_input("Size Range", "EU 38-44")
    need_size_chart = st.sidebar.checkbox("Include Shoe Size Chart?", value=True)

elif category == "Jewelry":
    attr1 = st.sidebar.selectbox("Metal", ["Gold", "Silver", "Bronze", "Iron", "Artificial"])
    attr2 = st.sidebar.text_input("Stone", "None")
    need_size_chart = False

elif category == "Stationery":
    # RESTORED MULTI-SELECT
    attr1 = st.sidebar.multiselect("Select Items", 
        ["Pencil", "Eraser", "Sharpener", "Scale", "Geometry Box", "Journal", "Pen", "Color Pencils", "Color Markers"], 
        default=["Pencil"])
    attr2 = st.sidebar.text_input("Pack Quantity", "1 set")
    need_size_chart = False

else: # Paper Soap
    attr1 = st.sidebar.text_input("Scent", "Floral")
    attr2 = st.sidebar.text_input("Quantity", "Pack of 5")
    need_size_chart = False

prod_name = st.sidebar.text_input("Product Name", "New Collection")
focus_kw = st.sidebar.text_input("Focus Keyword", "premium")
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
    uploaded_files = st.file_uploader("Upload Photos", type=['jpg', 'png', 'webp', 'jpeg'], accept_multiple_files=True)
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
        if category == "Clothing":
            st.subheader("📏 Clothing Size Chart (Inches)")
            size_data = {
                "Size": ["XS", "S", "M", "L", "XL", "XXL"],
                "Chest": ["34", "36", "38", "40", "44", "48"],
                "Waist": ["28", "30", "32", "34", "38", "42"],
                "Length": ["27", "28", "29", "30", "31", "32"]
            }
        else: # Shoes
            st.subheader("👟 Shoe Size Conversion")
            size_data = {
                "EU Size": ["38", "39", "40", "41", "42", "43", "44"],
                "UK Size": ["5", "6", "6.5", "7.5", "8", "9", "10"],
                "US Size (Men)": ["5.5", "6.5", "7.5", "8.5", "9", "10", "11"]
            }
        
        df = pd.DataFrame(size_data)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Chart (CSV)", data=csv, file_name=f"{category}_size_chart.csv", mime="text/csv")

# --- TAB 3: AI PROMPT HUB ---
with tab3:
    if generate_btn:
        st.success("✅ SEO Prompt Generated")
        prompt_text = f"""
        Act as a Senior E-commerce SEO Copywriter for ChatGPT & Gemini.
        Product: {prod_name} ({gender if gender else ''} {category})
        Attributes: {attr1}, {attr2}
        Focus Keyword: {focus_kw}
        Additional Info: {extra_details}

        Requirements:
        1. SEO Meta Title (75 chars)
        2. Meta Description (160 chars) - Start with focus keyword.
        3. URL Slug (include focus keyword).
        4. Short Description with H1 Heading.
        5. Long, humanized blog-style product story.
        6. 10 High-volume SEO tags.
        """
        st.code(prompt_text, language="markdown")
