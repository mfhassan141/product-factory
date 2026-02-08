import streamlit as st
from PIL import Image
import io
import zipfile
from datetime import datetime
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Product Factory Pro", layout="wide", initial_sidebar_state="expanded")

# --- MODERN DARK SUITE UI STYLING (FIXED VISIBILITY) ---
st.markdown("""
    <style>
        .stApp { background-color: #0E1117; color: #FFFFFF; }
        [data-testid="stSidebar"] { background-color: #161B22; border-right: 1px solid #30363D; }
        
        /* FIX: Sidebar Label Visibility - Force White/Blue */
        .stWidgetLabel p, label, .stSelectbox label, .stTextInput label, .stRadio label { 
            color: #58A6FF !important; 
            font-weight: bold !important; 
            font-size: 15px !important; 
            opacity: 1 !important;
        }
        
        /* Input Field Styling */
        .stTextInput input, .stSelectbox div, .stTextArea textarea {
            background-color: #0E1117 !important;
            color: white !important;
            border: 1px solid #30363D !important;
        }

        /* FIX: Browse Files Button */
        [data-testid="stFileUploadDropzone"] button {
            background-color: #58A6FF !important;
            color: #0E1117 !important;
            font-weight: bold !important;
        }

        /* Metric & Tabs */
        div[data-testid="stMetricValue"] { color: #58A6FF !important; font-family: 'Courier New', monospace; }
        .stTabs [data-baseweb="tab--active"] { color: #58A6FF !important; border-bottom: 2px solid #58A6FF !important; }
        
        /* Buttons */
        .stButton>button {
            width: 100%; border-radius: 8px; border: 1px solid #58A6FF;
            background-color: transparent; color: #58A6FF; font-weight: bold;
        }
        .stButton>button:hover { background-color: #58A6FF; color: #0E1117; }
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
    attr1 = st.sidebar.multiselect("Select Items", ["Pencil", "Eraser", "Sharpener", "Scale", "Geometry Box", "Journal", "Pen", "Color Pencils", "Color Markers"], default=["Pencil"])
    attr2 = st.sidebar.text_input("Pack Quantity", "1 set")
else:
    attr1 = st.sidebar.text_input("Scent", "Floral")
    attr2 = st.sidebar.text_input("Quantity", "Pack of 5")

prod_name = st.sidebar.text_input("Product Name", "Classic Collection")
focus_kw = st.sidebar.text_input("Focus Keyword", "premium quality")
extra_details = st.sidebar.text_area("Further Product Details", placeholder="Enter specific features, benefits, or care instructions...")

# --- PROMPT LOGIC (ChatGPT & Gemini Optimized) ---
gen_prompt = f"""
Act as a Senior E-commerce SEO Copywriter for ChatGPT and Gemini. 
Product: {prod_name} ({gender if gender else ''} {category})
Focus Keyword: {focus_kw}
Attributes: {attr1}, {attr2}
Additional Details: {extra_details}

Please write:
1. Meta Title: Standard SEO (max 75 chars), include Focus Keyword.
2. Meta Description: Persuasive, starts with Focus Keyword (max 160 chars).
3. URL Slug: Hyphenated, include Focus Keyword (max 60 chars).
4. Short Description: An engaging H1 Heading including the Focus Keyword, followed by a 2-3 sentence punchy summary.
5. Long SEO Description: A humanized, blog-style product story. Use an SEO-optimized structure with subheadings, bullet points for features, and a conclusion. Focus on benefit-driven language and weave in the focus keyword naturally.
6. 10 SEO Tags: High-volume hashtags and tags separated by commas.
"""

st.sidebar.divider()
generate_btn = st.sidebar.button("✨ GENERATE AI PROMPT")
generated_sku = f"{category[:2].upper()}-{prod_name[:3].upper()}-{datetime.now().strftime('%M%S')}"

# --- MAIN AREA ---
st.title("🚀 PRODUCT CONTENT FACTORY")
tab1, tab2, tab3 = st.tabs(["📸 IMAGE CONVERTER", "📈 PROFIT CALCULATOR", "♊ AI PROMPT HUB"])

# --- TAB 1: IMAGE CONVERTER ---
with tab1:
    st.subheader("Lightweight WebP Optimizer for WordPress")
    t_col1, t_col2 = st.columns([2, 1])
    with t_col2:
        target_size = st.selectbox("Export Size (Pixels)", [800, 1000, 1200], index=1)
        st.info("Files will be exported as highly compressed WebP for fast site loading.")
    
    with t_col1:
        uploaded_files = st.file_uploader("Upload Product Photos", type=['jpg', 'jpeg', 'png', 'webp'], accept_multiple_files=True)
    
    if uploaded_files:
        cols = st.columns(4)
        zip_buffer = io.BytesIO()
        count_opt, count_skip = 0, 0
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for idx, uploaded_file in enumerate(uploaded_files):
                f_name = uploaded_file.name
                # Process all to ensure target size and white background for WordPress uniformity
                img = Image.open(uploaded_file).convert("RGB")
                new_img = Image.new("RGB", (target_size, target_size), (255, 255, 255))
                img.thumbnail((target_size, target_size))
                offset = ((target_size-img.size[0])//2, (target_size-img.size[1])//2)
                new_img.paste(img, offset)
                
                img_io = io.BytesIO()
                # quality=75 is the 'sweet spot' for WordPress speed vs quality
                new_img.save(img_io, "WEBP", quality=75, method=6)
                img_bytes = img_io.getvalue()
                f_name = f"{f_name.split('.')[0]}.webp"
                count_opt += 1

                zip_file.writestr(f_name, img_bytes)
                with cols[idx % 4]:
                    st.image(img_bytes, caption=f_name)
                    st.caption("⚙️ WordPress Optimized")
        
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
    st.subheader("AI SEO Prompt for ChatGPT & Gemini")
    if generate_btn:
        st.success("✅ Your humanized SEO prompt is ready!")
        st.code(gen_prompt, language="markdown")
        st.info("💡 Copy the code above and paste it into ChatGPT or Gemini for a full SEO product page.")
    else:
        st.warning("Please fill details in the Sidebar and click 'Generate AI Prompt'.")
