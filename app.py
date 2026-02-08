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
        .stButton>button:hover { background-color: #357ABD !important; }

        .stTabs [data-baseweb="tab--active"] {
            color: #4A90E2 !important; border-bottom: 2px solid #4A90E2 !important;
        }

        .stDownloadButton>button {
            background-color: #52B788 !important; color: #FFFFFF !important;
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

elif category == "Jewelry":
    attr1 = st.sidebar.selectbox("Metal", ["Gold", "Silver", "Bronze", "Iron", "Artificial"])
    attr2 = st.sidebar.text_input("Stone", "None")
    need_size_chart = False

elif category == "Stationery":
    attr1 = st.sidebar.multiselect("Select Items", 
        ["Pencil", "Eraser", "Sharpener", "Scale", "Geometry Box", "Journal", "Pen", "Color Pencils", "Color Markers"], 
        default=["Pencil"])
    attr2 = st.sidebar.text_input("Pack Quantity", "1 set")
    need_size_chart = False

else:
    attr1 = st.sidebar.text_input("Scent", "Floral")
    attr2 = st.sidebar.text_input("Quantity", "Pack of 5")
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
        prompt_text = f"Product: {prod_name} | Keyword: {focus_kw} | Category: {category} | Group: {attr2}"
        st.code(prompt_text, language="markdown")

# --- TAB 4: ENHANCED DYNAMIC SIZE CHART HUB ---
with tab4:
    if need_size_chart:
        st.subheader(f"Detailed Sizing: {attr2}")
        
        # --- ENHANCED DYNAMIC DATA LOGIC ---
        if category == "Clothing":
            if attr2 == "Newly Born":
                data = {
                    "Age (Months)": ["0-3M", "3-6M", "6-9M", "9-12M"],
                    "Chest (in)": ["17", "18", "18.5", "19"],
                    "Length (in)": ["14", "15.5", "16.5", "18"]
                }
            elif attr2 == "Child":
                data = {
                    "Age Range": ["1-2Y", "2-3Y", "3-4Y", "4-5Y", "5-6Y"],
                    "Chest (in)": ["20-21", "21-22", "22-23", "23-24", "24-25"],
                    "Length (in)": ["16", "18", "20", "22", "24"],
                    "Waist (in)": ["19-20", "20-20.5", "20.5-21", "21-21.5", "21.5-22"]
                }
            elif attr2 == "Teenage":
                data = {
                    "Size": ["S", "M", "L", "XL", "XXL"],
                    "Chest (in)": ["30-32", "32-34", "34-36", "36-38", "38-40"],
                    "Waist (in)": ["24-25", "26-27", "28-29", "30-31", "32-33"],
                    "Length (in)": ["24", "25", "26", "27", "28"]
                }
            else: # Adult
                data = {
                    "Size": ["S", "M", "L", "XL", "XXL", "XXXL"],
                    "Chest (in)": ["36-38", "39-41", "42-44", "45-47", "48-50", "51-53"],
                    "Waist (in)": ["30-32", "33-35", "36-38", "39-41", "42-44", "45-47"],
                    "Length (in)": ["27", "28", "29", "30", "31", "32"]
                }
        else: # Shoes
            data = {
                "EU": ["38", "39", "40", "41", "42", "43", "44"],
                "UK": ["5", "6", "6.5", "7.5", "8", "9", "10"],
                "US": ["5.5", "6.5", "7.5", "8.5", "9", "10", "11"]
            }
        
        df = pd.DataFrame(data)

        # DOWNLOAD & COPY INSTRUCTION
        b1, b2 = st.columns([1, 4])
        with b1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📊 DOWNLOAD CSV", data=csv, file_name=f"{attr2}_size_chart.csv", mime="text/csv")
        with b2:
            st.info("👆 Download for Excel/Sheets or highlight and copy (Ctrl+C) the table below for Word.")

        # DISPLAY ENHANCED TABLE
        st.table(df)
        
    else:
        st.info("Please select 'Clothing' or 'Shoes' and enable the Size Chart checkbox in the sidebar.")
