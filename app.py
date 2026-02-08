import streamlit as st
from PIL import Image
import io
import zipfile
from datetime import datetime
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="Product Factory Pro", layout="wide", initial_sidebar_state="expanded")

# --- UI STYLING: DIM SOFT MODE ---
st.markdown("""
    <style>
        .stApp { background-color: #F0F2F6; color: #31333F; }
        [data-testid="stSidebar"] { background-color: #E6E9EF; border-right: 1px solid #D1D5DB; }
        h1, h2, h3, h4, label, .stWidgetLabel p { color: #262730 !important; font-family: 'Inter', sans-serif; }
        
        .stTextInput input, .stSelectbox div, .stTextArea textarea, .stNumberInput input {
            background-color: #FFFFFF !important; color: #31333F !important;
            border: 1px solid #C4C9D0 !important; border-radius: 8px !important;
        }

        .stButton>button {
            width: 100%; border-radius: 8px; border: none;
            background-color: #4A90E2 !important; color: #FFFFFF !important;
            font-weight: 600 !important; cursor: pointer !important;
        }
        
        .comparison-text {
            font-size: 0.8rem;
            color: #555E6D;
            line-height: 1.2;
        }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: PROMPT GENERATOR ---
st.sidebar.title("🤖 AI Prompt Studio")
currency = st.sidebar.selectbox("Currency", ["PKR", "USD", "AED", "GBP", "EUR"])
category = st.sidebar.selectbox("Category", ["Clothing", "Shoes", "Jewelry", "Stationery", "Paper Soap"])

attr1, attr2, gender = "", "", ""

if category == "Clothing":
    gender = st.sidebar.radio("Target Gender", ["Male", "Female", "Unisex"])
    fabric_choice = st.sidebar.selectbox("Fabric", ["Cotton", "Lawn", "Silk", "Linen", "Chiffon", "Jersey", "Wool", "Other"])
    attr1 = st.sidebar.text_input("Manual Fabric Entry") if fabric_choice == "Other" else fabric_choice
    attr2 = st.sidebar.selectbox("Age Group", ["Newly Born", "Child", "Teenage", "Adult"])
    need_size_chart = st.sidebar.checkbox("Enable Size Chart Tab?", value=True)

elif category == "Shoes":
    gender = st.sidebar.radio("Target Gender", ["Male", "Female", "Unisex"])
    attr1 = st.sidebar.text_input("Material", "Leather")
    attr2 = st.sidebar.text_input("Size Range", "EU 38-44")
    need_size_chart = st.sidebar.checkbox("Enable Shoe Size Tab?", value=True)

elif category == "Stationery":
    items = st.sidebar.multiselect("Select Items", 
        ["Pencil", "Eraser", "Sharpener", "Scale", "Geometry Box", "Journal", "Pen", "Color Pencils", "Color Markers"], 
        default=["Pencil"])
    
    # NEW LOGIC: If Geometry Box is selected, ask for contents
    geo_contents = ""
    if "Geometry Box" in items:
        st.sidebar.info("📐 Geometry Box Details")
        content_list = st.sidebar.multiselect("Geometry Box contains:", 
            ["Empty", "Pencil", "Eraser", "Sharpener", "Scale", "Compass", "Divider", "Protractor", "Set Squares"],
            default=["Empty"])
        geo_contents = f"(Contains: {', '.join(content_list)})"
    
    attr1 = f"Items: {', '.join(items)} {geo_contents}"
    attr2 = st.sidebar.text_input("Pack Quantity", "1 set")
    need_size_chart = False

else: # Paper Soap / Jewelry
    attr1 = st.sidebar.text_input("Specific Attribute")
    attr2 = st.sidebar.text_input("Quantity/Spec")
    need_size_chart = False

prod_name = st.sidebar.text_input("Product Name", "New Collection")
focus_kw = st.sidebar.text_input("Focus Keyword", "premium quality")
extra_details = st.sidebar.text_area("Extra Details")

st.sidebar.divider()
generate_btn = st.sidebar.button("✨ GENERATE AI PROMPT")

# --- MAIN AREA ---
st.title("🚀 Product Content Factory")
tab1, tab2, tab3, tab4 = st.tabs(["📸 IMAGE CONVERTER", "📈 PROFIT CALCULATOR", "♊ AI PROMPT HUB", "📏 SIZE CHART HUB"])

# --- TAB 1: IMAGE CONVERTER ---
with tab1:
    st.subheader("WordPress Optimized WebP Converter")
    target_size = st.selectbox("Export Size (Pixels)", [800, 1000, 1200], index=1)
    uploaded_files = st.file_uploader("Upload Photos", type=['jpg', 'png', 'webp', 'jpeg'], accept_multiple_files=True)
    
    if uploaded_files:
        zip_buffer = io.BytesIO()
        comparison_data = []

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for uploaded_file in uploaded_files:
                orig_bytes = uploaded_file.getvalue()
                orig_kb = len(orig_bytes) / 1024
                img = Image.open(uploaded_file).convert("RGB")
                orig_w, orig_h = img.size
                
                new_img = Image.new("RGB", (target_size, target_size), (255, 255, 255))
                img.thumbnail((target_size, target_size))
                offset = ((target_size-img.size[0])//2, (target_size-img.size[1])//2)
                new_img.paste(img, offset)
                
                img_io = io.BytesIO()
                new_img.save(img_io, "WEBP", quality=75)
                new_bytes = img_io.getvalue()
                new_kb = len(new_bytes) / 1024
                
                reduction = ((orig_kb - new_kb) / orig_kb) * 100 if orig_kb > 0 else 0
                comparison_data.append({
                    "Name": uploaded_file.name,
                    "Orig": f"{orig_w}x{orig_h} ({orig_kb:.1f} KB)",
                    "New": f"{target_size}x{target_size} ({new_kb:.1f} KB)",
                    "Saved": f"{reduction:.1f}%"
                })
                zip_file.writestr(f"{uploaded_file.name.split('.')[0]}.webp", new_bytes)

        st.download_button("📦 DOWNLOAD IMAGES (ZIP)", zip_buffer.getvalue(), "images.zip")
        
        st.markdown("---")
        st.markdown("<p class='comparison-text'><b>📊 CONVERSION ANALYSIS:</b></p>", unsafe_allow_html=True)
        for item in comparison_data:
            st.markdown(f"<p class='comparison-text'><b>{item['Name']}</b>: From {item['Orig']} to {item['New']} | <b>REDUCTION: {item['Saved']}</b></p>", unsafe_allow_html=True)

# --- TAB 2: PROFIT CALCULATOR ---
with tab2:
    st.subheader("Profit Breakdown")
    c1, c2 = st.columns(2)
    cost_p = c1.number_input(f"Cost Price", min_value=0.0)
    sell_p = c2.number_input(f"Selling Price", min_value=0.0)
    st.metric("Net Profit", f"{currency} {sell_p - cost_p:,.2f}")

# --- TAB 3: AI PROMPT HUB ---
with tab3:
    if generate_btn:
        st.success("✅ SEO Prompt Generated")
        # Included the specific Stationery attributes in the generated prompt
        prompt_text = f"Act as SEO Copywriter. Product: {prod_name}. Category: {category}. Attributes: {attr1}. Keyword: {focus_kw}."
        st.code(prompt_text, language="markdown")

# --- TAB 4: SIZE CHART HUB ---
with tab4:
    if need_size_chart:
        st.subheader(f"Detailed Sizing: {attr2}")
        if category == "Clothing":
            if attr2 == "Teenage": 
                data = {"Size": ["S", "M", "L", "XL"], "Chest": ["30-32","32-34","34-36","36-38"], "Waist": ["24","26","28","30"], "Length": ["24","25","26","27"]}
            elif attr2 == "Adult": 
                data = {"Size": ["S", "M", "L", "XL"], "Chest": ["38-40","42-44","46-48","50-52"], "Waist": ["32","34","36","38"], "Length": ["28","29","30","31"]}
            elif attr2 == "Child":
                data = {"Age Range": ["1-2Y", "2-3Y", "3-4Y", "4-5Y"], "Chest": ["20-21", "21-22", "22-23", "23-24"], "Length": ["16", "18", "20", "22"]}
            elif attr2 == "Newly Born":
                data = {"Age": ["0-3M", "3-6M", "6-9M", "9-12M"], "Chest": ["17", "18", "18.5", "19"], "Length": ["14", "15.5", "16.5", "18"]}
            
            df = pd.DataFrame(data)
            st.table(df)
            st.download_button("📊 DOWNLOAD CSV", data=df.to_csv(index=False).encode('utf-8'), file_name=f"{attr2}_size_chart.csv")
    else:
        st.info("Size charts are available for Clothing and Shoes.")
