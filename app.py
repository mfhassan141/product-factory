import streamlit as st
from PIL import Image
import io
import zipfile
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Product Factory Core", layout="wide")

st.title("🛠️ Product Content Factory")
st.markdown("Resize images to WebP and manage product data without AI.")

# --- SIDEBAR: DYNAMIC PRODUCT DATA ---
st.sidebar.header("📝 Product Configuration")

# 1. Category Selection
category = st.sidebar.selectbox(
    "Select Category", 
    ["Clothing", "Shoes", "Jewelry", "Stationery", "Paper Soap"]
)

# 2. Dynamic Inputs based on Category
attr1, attr2 = "", ""
if category == "Clothing":
    attr1 = st.sidebar.text_input("Fabric", placeholder="e.g. Cotton Jersey")
    attr2 = st.sidebar.text_input("Age Group", placeholder="1-10y")
elif category == "Shoes":
    attr1 = st.sidebar.text_input("Material", placeholder="e.g. Leather")
    attr2 = st.sidebar.text_input("Size Range", placeholder="EU 38-44")
elif category == "Jewelry":
    attr1 = st.sidebar.text_input("Metal", placeholder="e.g. 24k Gold")
    attr2 = st.sidebar.text_input("Gemstone", placeholder="e.g. Diamond")
elif category == "Stationery":
    attr1 = st.sidebar.text_input("Item Type", placeholder="e.g. Planner")
    attr2 = st.sidebar.text_input("Paper Quality", placeholder="e.g. 100gsm")
else: # Paper Soap
    attr1 = st.sidebar.text_input("Scent", placeholder="e.g. Lemon")
    attr2 = st.sidebar.text_input("Pack Size", placeholder="Pack of 3")

prod_name = st.sidebar.text_input("Product Name", placeholder="e.g. Girls Tracksuit")
primary_kw = st.sidebar.text_input("Primary Keyword", placeholder="girls summer wear")

st.sidebar.markdown("---")

# 3. Profit Calculator
st.sidebar.subheader("💰 Profit Calculator")
cost_p = st.sidebar.number_input("Cost Price", min_value=0.0, value=0.0)
sell_p = st.sidebar.number_input("Selling Price", min_value=0.0, value=1000.0)
tax_r = st.sidebar.slider("Tax/GST %", 0, 25, 18)

net_p = sell_p - (cost_p + (sell_p * (tax_r/100)))
st.sidebar.metric("Expected Profit", f"{net_p:,.2f}", f"{(net_p/sell_p)*100 if sell_p > 0 else 0:.1f}% Margin")

st.sidebar.markdown("---")
target_size = st.sidebar.selectbox(
    "Image Size (px)", options=[800, 1000, 1200], index=1
)

# --- SKU GENERATOR ---
cat_code = category[:2].upper()
brd_code = prod_name[:3].upper() if prod_name else "GEN"
generated_sku = f"{cat_code}-{brd_code}-{datetime.now().strftime('%M%S')}"

# --- MAIN AREA ---
uploaded_files = st.file_uploader("Upload Product Images", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if uploaded_files:
    st.subheader("🖼️ Processed Images")
    cols = st.columns(4)
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for idx, uploaded_file in enumerate(uploaded_files):
            img = Image.open(uploaded_file).convert("RGB")
            new_img = Image.new("RGB", (target_size, target_size), (255, 255, 255))
            img.thumbnail((target_size, target_size))
            offset = ((target_size - img.size[0]) // 2, (target_size - img.size[1]) // 2)
            new_img.paste(img, offset)
            
            img_io = io.BytesIO()
            new_img.save(img_io, "WEBP", quality=85)
            img_bytes = img_io.getvalue()
            
            file_name = f"{uploaded_file.name.split('.')[0]}.webp"
            zip_file.writestr(file_name, img_bytes)
            
            with cols[idx % 4]:
                st.image(img_bytes, caption=file_name)

    st.download_button("📦 Download All as ZIP", data=zip_buffer.getvalue(), 
                       file_name=f"products_{datetime.now().strftime('%H%M%S')}.zip", mime="application/zip")

    st.divider()
    st.subheader("📋 Product Summary (No AI)")
    
    st.success(f"**SKU:** {generated_sku}")
    st.write(f"**Category:** {category} | **Brand:** {prod_name}")
    st.write(f"**Specs:** {attr1}, {attr2}")
    st.write(f"**Target Price:** {sell_p}")

else:
    st.warning("Please upload images to begin.")
