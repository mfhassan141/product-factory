import streamlit as st
from PIL import Image
import io
import zipfile
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Product Factory Pro", layout="wide", initial_sidebar_state="expanded")

# --- MODERN DARK SUITE UI STYLING ---
st.markdown("""
    <style>
        /* Main background and text */
        .stApp {
            background-color: #0E1117;
            color: #FFFFFF;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #161B22;
            border-right: 1px solid #30363D;
        }
        
        /* Custom Card UI */
        .status-card {
            background-color: #1c2128;
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 10px;
        }

        /* Metric styling */
        div[data-testid="stMetricValue"] {
            color: #58A6FF !important;
            font-family: 'Courier New', monospace;
            font-weight: bold;
        }
        
        /* Button styling */
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            border: 1px solid #58A6FF;
            background-color: transparent;
            color: #58A6FF;
            font-weight: bold;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #58A6FF;
            color: #0E1117;
            box-shadow: 0 0 15px rgba(88, 166, 255, 0.4);
        }

        /* Header styling */
        h1, h2, h3 {
            color: #58A6FF !important;
            letter-spacing: 1px;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #161B22;
            border: 1px solid #30363D;
            border-radius: 5px 5px 0px 0px;
            padding: 10px 20px;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: DYNAMIC PRODUCT DATA ---
st.sidebar.header("🕹️ CONTROL PANEL")

category = st.sidebar.selectbox(
    "Category", 
    ["Clothing", "Shoes", "Jewelry", "Stationery", "Paper Soap"]
)

# Category-specific logic
attr1, attr2 = "", ""
if category == "Clothing":
    attr1 = st.sidebar.text_input("Fabric", "Cotton")
    attr2 = st.sidebar.text_input("Age Group", "Adult")
elif category == "Shoes":
    attr1 = st.sidebar.text_input("Material", "Leather")
    attr2 = st.sidebar.text_input("Size", "EU 42")
elif category == "Jewelry":
    attr1 = st.sidebar.text_input("Metal", "Gold")
    attr2 = st.sidebar.text_input("Stone", "None")
elif category == "Stationery":
    attr1 = st.sidebar.text_input("Type", "Journal")
    attr2 = st.sidebar.text_input("Paper", "100gsm")
else:
    attr1 = st.sidebar.text_input("Scent", "Floral")
    attr2 = st.sidebar.text_input("Quantity", "Pack of 5")

prod_name = st.sidebar.text_input("Product Name", "New Arrival")
target_size = st.sidebar.selectbox("Export Size", [800, 1000, 1200], index=1)

st.sidebar.divider()

# SKU Logic
cat_code = category[:2].upper()
brd_code = prod_name[:3].upper() if prod_name else "GEN"
generated_sku = f"{cat_code}-{brd_code}-{datetime.now().strftime('%M%S')}"

# --- APP LAYOUT ---
st.title("🚀 PRODUCT CONTENT FACTORY")

tab1, tab2 = st.tabs(["📸 IMAGE STUDIO", "📈 BUSINESS INTELLIGENCE"])

with tab1:
    st.subheader("Image Optimization Engine")
    uploaded_files = st.file_uploader("Drop images here", type=['jpg', 'jpeg', 'png', 'webp'], accept_multiple_files=True)

    if uploaded_files:
        cols = st.columns(4)
        zip_buffer = io.BytesIO()
        count_opt, count_skip = 0, 0

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            for idx, uploaded_file in enumerate(uploaded_files):
                f_name = uploaded_file.name
                
                if f_name.lower().endswith('.webp'):
                    img_bytes = uploaded_file.getvalue()
                    status = "✅ SKIP (WebP)"
                    count_skip += 1
                else:
                    img = Image.open(uploaded_file).convert("RGB")
                    new_img = Image.new("RGB", (target_size, target_size), (255, 255, 255))
                    img.thumbnail((target_size, target_size))
                    offset = ((target_size - img.size[0]) // 2, (target_size - img.size[1]) // 2)
                    new_img.paste(img, offset)
                    
                    img_io = io.BytesIO()
                    new_img.save(img_io, "WEBP", quality=85)
                    img_bytes = img_io.getvalue()
                    f_name = f"{f_name.split('.')[0]}.webp"
                    status = "⚙️ OPTIMIZED"
                    count_opt += 1

                zip_file.writestr(f_name, img_bytes)
                with cols[idx % 4]:
                    st.image(img_bytes, caption=f_name)
                    st.caption(status)

        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Files", len(uploaded_files))
        m2.metric("Converted", count_opt)
        m3.metric("Bypassed", count_skip)

        st.download_button("📦 DOWNLOAD PROCESSED BUNDLE (ZIP)", zip_buffer.getvalue(), 
                           f"factory_{datetime.now().strftime('%H%M')}.zip", "application/zip")

with tab2:
    st.subheader("Financial & Inventory Specs")
    
    col_a, col_b = st.columns(2)
    with col_a:
        cost_p = st.number_input("Cost Price", value=0.0)
        sell_p = st.number_input("Selling Price", value=100.0)
    with col_b:
        tax_r = st.slider("Tax/VAT %", 0, 25, 18)
        
    # Calculations
    tax_amt = sell_p * (tax_r / 100)
    net_profit = sell_p - (cost_p + tax_amt)
    margin = (net_profit / sell_p * 100) if sell_p > 0 else 0

    with st.container(border=True):
        st.write("### 💰 Profit Summary")
        m_a, m_b, m_c = st.columns(3)
        m_a.metric("Tax Deducted", f"-{tax_amt:.2f}")
        m_b.metric("Final Profit", f"{net_profit:,.2f}")
        m_c.metric("Profit Margin", f"{margin:.1f}%")

    with st.container(border=True):
        st.write("### 📋 Production Metadata")
        st.markdown(f"**Generated SKU:** `{generated_sku}`")
        st.markdown(f"**Spec Summary:** {category} | {attr1} | {attr2}")
