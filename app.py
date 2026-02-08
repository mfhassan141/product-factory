import streamlit as st
from PIL import Image
import io
import zipfile
from datetime import datetime
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Product Factory Pro", layout="wide", initial_sidebar_state="expanded")

# --- MODERN DARK SUITE UI STYLING ---
st.markdown("""
    <style>
        .stApp { background-color: #0E1117; color: #FFFFFF; }
        [data-testid="stSidebar"] { background-color: #161B22; border-right: 1px solid #30363D; }
        
        /* Sidebar Label Visibility */
        .stWidgetLabel p { color: #58A6FF !important; font-weight: bold; font-size: 16px; }
        
        /* Browse Files Button */
        [data-testid="stFileUploadDropzone"] button {
            background-color: #58A6FF !important;
            color: #0E1117 !important;
            font-weight: bold !important;
        }

        /* Metric & Tabs */
        div[data-testid="stMetricValue"] { color: #58A6FF !important; font-family: 'Courier New', monospace; }
        .stTabs [data-baseweb="tab--active"] { color: #58A6FF !important; border-bottom: 2px solid #58A6FF !important; }

        /* Tables Styling */
        .styled-table { margin: 25px 0; font-size: 0.9em; min-width: 400px; border-radius: 5px 5px 0 0; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: PROMPT GENERATOR ---
st.sidebar.header("🤖 PROMPT GENERATOR")
currency = st.sidebar.selectbox("Currency", ["PKR", "USD", "AED", "GBP", "EUR"])
category = st.sidebar.selectbox("Category", ["Clothing", "Shoes", "Jewelry", "Stationery", "Paper Soap"])

attr1, attr2, gender = "", "", ""

if category in ["Clothing", "Shoes"]:
    gender = st.sidebar.radio("Target Gender", ["Male", "Female", "Unisex"])

if category == "Clothing":
    attr1 = st.sidebar.text_input("Fabric", "Cotton")
    attr2 = st.sidebar.text_input("Age Group", "Adult")
elif category == "Shoes":
    attr1 = st.sidebar.text_input("Material", "Leather")
    attr2 = st.sidebar.text_input("Size Range", "EU 38-44")
elif category == "Jewelry":
    attr1 = st.sidebar.selectbox("Metal", ["Gold", "Silver", "Bronze", "Iron", "Artificial"])
    attr2 = st.sidebar.text_input("Stone", "None")
elif category == "Stationery":
    attr1 = st.sidebar.selectbox("Item Type", ["Pencil", "Eraser", "Sharpener", "Scale", "Geometry Box", "Journal", "Pen"])
    attr2 = st.sidebar.text_input("Pack Quantity", "1 unit")
else:
    attr1 = st.sidebar.text_input("Scent", "Floral")
    attr2 = st.sidebar.text_input("Quantity", "Pack of 5")

prod_name = st.sidebar.text_input("Product Name", "Classic Collection")
focus_kw = st.sidebar.text_input("Focus Keyword", "premium quality")
target_size = st.sidebar.selectbox("Image Export Size", [800, 1000, 1200], index=1)

# Prompt Logic
gen_prompt = f"""
Act as an E-commerce SEO Expert. Generate content for:
- Product: {prod_name} ({gender} {category})
- Specifics: {attr1}, {attr2}
- Target Keyword: {focus_kw}

Please provide:
1. Meta Title: Standard SEO style (max 75 chars), include Focus Keyword.
2. Meta Description: Start with the Focus Keyword (max 160 chars).
3. URL Slug: Clean, hyphenated (max 60 chars), include Focus Keyword.
4. SEO Tags: 10 relevant tags/hashtags separated by commas.
"""

st.sidebar.divider()
generate_btn = st.sidebar.button("✨ GENERATE GEMINI PROMPT")
generated_sku = f"{category[:2].upper()}-{prod_name[:3].upper()}-{datetime.now().strftime('%M%S')}"

# --- MAIN AREA ---
st.title("🚀 PRODUCT CONTENT FACTORY")
tab1, tab2, tab3 = st.tabs(["📸 IMAGE CONVERTER", "📈 PROFIT CALCULATOR", "♊ GEMINI PROMPT"])

# --- TAB 1: IMAGE CONVERTER ---
with tab1:
    st.subheader("Image Optimization Engine")
    uploaded_files = st.file_uploader("Upload Images", type=['jpg', 'jpeg', 'png', 'webp'], accept_multiple_files=True)
    if uploaded_files:
        cols = st.columns(4)
        zip_buffer = io.BytesIO()
        count_opt, count_skip = 0, 0
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for idx, uploaded_file in enumerate(uploaded_files):
                f_name = uploaded_file.name
                if f_name.lower().endswith('.webp'):
                    img_bytes = uploaded_file.getvalue()
                    status, count_skip = "✅ WebP", count_skip + 1
                else:
                    img = Image.open(uploaded_file).convert("RGB")
                    new_img = Image.new("RGB", (target_size, target_size), (255, 255, 255))
                    img.thumbnail((target_size, target_size))
                    offset = ((target_size-img.size[0])//2, (target_size-img.size[1])//2)
                    new_img.paste(img, offset)
                    img_io = io.BytesIO()
                    new_img.save(img_io, "WEBP", quality=85)
                    img_bytes = img_io.getvalue()
                    f_name = f"{f_name.split('.')[0]}.webp"
                    status, count_opt = "⚙️ Optimized", count_opt + 1
                zip_file.writestr(f_name, img_bytes)
                with cols[idx % 4]:
                    st.image(img_bytes, caption=f_name)
                    st.caption(status)
        st.download_button("📦 DOWNLOAD ALL (ZIP)", zip_buffer.getvalue(), f"files_{datetime.now().strftime('%H%M')}.zip")

# --- TAB 2: PROFIT CALCULATOR & SIZE CHART ---
with tab2:
    st.subheader("Financial Breakdown")
    col_a, col_b = st.columns(2)
    with col_a:
        cost_p = st.number_input(f"Cost Price ({currency})", value=0.0)
        sell_p = st.number_input(f"Selling Price ({currency})", value=100.0)
    with col_b:
        tax_r = st.slider("Tax/VAT %", 0, 25, 18)
    
    tax_amt = sell_p * (tax_r / 100)
    net_profit = sell_p - (cost_p + tax_amt)
    margin = (net_profit / sell_p * 100) if sell_p > 0 else 0

    st.container(border=True).metric("Final Profit", f"{currency} {net_profit:,.2f}", f"{margin:.1f}% Margin")

    # Dynamic Size Chart for Clothing
    if category == "Clothing":
        st.divider()
        st.subheader("📏 Standard Clothing Size Chart (Inches)")
        size_data = {
            "Size": ["XS", "S", "M", "L", "XL", "XXL"],
            "Chest": ["34-36", "36-38", "38-40", "42-44", "46-48", "50-52"],
            "Waist": ["28-30", "30-32", "32-34", "36-38", "40-42", "44-46"],
            "Length": ["27", "28", "29", "30", "31", "32"]
        }
        df_size = pd.DataFrame(size_data)
        st.table(df_size)
        st.info("💡 Standard US/EU sizing. Adjust according to your specific brand measurements.")

# --- TAB 3: GEMINI PROMPT ---
with tab3:
    st.subheader("Gemini SEO Prompt")
    if generate_btn:
        st.success("✅ Your prompt is ready!")
        st.code(gen_prompt, language="markdown")
    else:
        st.warning("Please fill details in the Sidebar and click 'Generate Prompt'.")

if generate_btn:
    st.info(f"👉 **SKU Created:** `{generated_sku}`")
