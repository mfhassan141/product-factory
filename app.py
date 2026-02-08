import streamlit as st
from PIL import Image
import io
import zipfile
from datetime import datetime
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Product Factory Pro", layout="wide", initial_sidebar_state="expanded")

# --- UI STYLING (WHITE TITLES, BLACK BUTTON TEXT) ---
st.markdown("""
    <style>
        .stApp { background-color: #0E1117; color: #FFFFFF; }
        [data-testid="stSidebar"] { background-color: #161B22; border-right: 1px solid #30363D; }
        
        /* Force All Labels and Titles to WHITE */
        .stWidgetLabel p, label, .stSelectbox label, .stTextInput label, .stRadio label, h1, h2, h3, h4, h5, h6 { 
            color: #FFFFFF !important; 
            font-weight: bold !important; 
            opacity: 1 !important;
        }
        
        /* Sidebar Titles specifically */
        [data-testid="stSidebar"] .stWidgetLabel p { color: #FFFFFF !important; }

        /* FIX: Button Background Blue, Text BLACK */
        .stButton>button {
            width: 100%; border-radius: 8px; border: none;
            background-color: #58A6FF !important; 
            color: #000000 !important; /* Black text */
            font-weight: bold !important;
        }
        .stButton>button:hover { 
            background-color: #FFFFFF !important; 
            color: #000000 !important; 
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.4); 
        }

        /* File Uploader Button Fix */
        [data-testid="stFileUploadDropzone"] button {
            background-color: #58A6FF !important;
            color: #000000 !important;
            font-weight: bold !important;
        }
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
    # 1. FABRIC DROPDOWN WITH MANUAL INPUT
    fabric_list = ["Cotton", "Lawn", "Silk", "Linen", "Chiffon", "Jersey", "Denim", "Wool", "Polyester", "Velvet", "Other (Manual)"]
    fabric_choice = st.sidebar.selectbox("Select Fabric", fabric_list)
    if fabric_choice == "Other (Manual)":
        attr1 = st.sidebar.text_input("Enter Fabric Type", placeholder="e.g. Bamboo Blend")
    else:
        attr1 = fabric_choice

    # 2. AGE GROUP DROPDOWN
    age_list = ["Newly Born", "Child", "Teenage", "Adult"]
    attr2 = st.sidebar.selectbox("Age Group", age_list)

elif category == "Shoes":
    attr1 = st.sidebar.text_input("Material", "Leather")
    attr2 = st.sidebar.text_input("Size Range", "EU 38-44")

elif category == "Jewelry":
    attr1 = st.sidebar.selectbox("Metal", ["Gold", "Silver", "Bronze", "Iron", "Artificial"])
    attr2 = st.sidebar.text_input("Stone", "None")

elif category == "Stationery":
    attr1 = st.sidebar.multiselect("Select Items", ["Pencil", "Eraser", "Sharpener", "Scale", "Geometry Box", "Journal", "Pen", "Color Pencils", "Color Markers"], default=["Pencil"])
    attr2 = st.sidebar.text_input("Pack Quantity", "1 set")

else:
    attr1 = st.sidebar.text_input("Scent", "Floral")
    attr2 = st.sidebar.text_input("Quantity", "Pack of 5")

prod_name = st.sidebar.text_input("Product Name", "Classic Collection")
focus_kw = st.sidebar.text_input("Focus Keyword", "premium quality")
extra_details = st.sidebar.text_area("Further Product Details", placeholder="Specific features, benefits, care instructions...")

# --- PROMPT LOGIC ---
gen_prompt = f"""
Act as a Senior E-commerce SEO Copywriter for ChatGPT and Gemini. 
Product: {prod_name} ({gender if gender else ''} {category})
Focus Keyword: {focus_kw}
Attributes: {attr1}, {attr2}
Details: {extra_details}

Please write:
1. Meta Title: Standard SEO (max 75 chars), include Focus Keyword.
2. Meta Description: Persuasive, starts with Focus Keyword (max 160 chars).
3. URL Slug: Hyphenated, include Focus Keyword (max 60 chars).
4. Short Description: An engaging H1 Heading including the Focus Keyword, followed by a punchy summary.
5. Long SEO Description: A humanized, blog-style product story. Use subheadings, bullet points, and a benefit-driven conclusion.
6. 10 SEO Tags: High-volume tags separated by commas.
"""

st.sidebar.divider()
generate_btn = st.sidebar.button("✨ GENERATE AI PROMPT")

# --- MAIN AREA ---
st.title("🚀 PRODUCT CONTENT FACTORY")
tab1, tab2, tab3 = st.tabs(["📸 IMAGE CONVERTER", "📈 PROFIT CALCULATOR", "♊ AI PROMPT HUB"])

# --- TAB 1: IMAGE CONVERTER ---
with tab1:
    st.subheader("WordPress Optimized WebP Converter")
    target_size = st.selectbox("Export Size (Pixels)", [800, 1000, 1200], index=1)
    uploaded_files = st.file_uploader("Upload Product Photos", type=['jpg', 'jpeg', 'png', 'webp'], accept_multiple_files=True)
    
    if uploaded_files:
        cols = st.columns(4)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for idx, uploaded_file in enumerate(uploaded_files):
                img = Image.open(uploaded_file).convert("RGB")
                new_img = Image.new("RGB", (target_size, target_size), (255, 255, 255))
                img.thumbnail((target_size, target_size))
                offset = ((target_size-img.size[0])//2, (target_size-img.size[1])//2)
                new_img.paste(img, offset)
                
                img_io = io.BytesIO()
                new_img.save(img_io, "WEBP", quality=75, method=6)
                img_bytes = img_io.getvalue()
                f_name = f"{uploaded_file.name.split('.')[0]}.webp"
                zip_file.writestr(f_name, img_bytes)
                with cols[idx % 4]:
                    st.image(img_bytes, caption=f_name)
        
        st.divider()
        st.download_button("📦 DOWNLOAD OPTIMIZED ZIP", zip_buffer.getvalue(), f"wp_images_{datetime.now().strftime('%M%S')}.zip")

# --- TAB 2: PROFIT CALCULATOR ---
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

    if category == "Clothing":
        st.divider()
        st.subheader("📏 Standard Size Reference")
        size_data = {"Size": ["XS", "S", "M", "L", "XL"], "Chest": ["34-36", "36-38", "38-40", "42-44", "46-48"], "Waist": ["28-30", "30-32", "32-34", "36-38", "40-42"]}
        st.table(pd.DataFrame(size_data))

# --- TAB 3: AI PROMPT HUB ---
with tab3:
    st.subheader("SEO Prompt for ChatGPT & Gemini")
    if generate_btn:
        st.success("✅ Your humanized SEO prompt is ready!")
        st.code(gen_prompt, language="markdown")
    else:
        st.warning("Complete the sidebar details and click 'Generate AI Prompt'.")
