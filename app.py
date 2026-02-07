import streamlit as st
from PIL import Image
import io
import zipfile
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Product Content Factory", layout="wide")

st.title("🛠️ Product Content Factory")
st.markdown("Upload images, resize them to WebP, and prepare data for Gemini.")

# --- SIDEBAR: PRODUCT DATA ---
st.sidebar.header("📝 Product Information")
prod_name = st.sidebar.text_input("Product Name", placeholder="e.g. Girls Tracksuit")
prod_fabric = st.sidebar.text_input("Fabric", placeholder="e.g. Cotton Jersey")
prod_age = st.sidebar.text_input("Age Group", placeholder="1-10y")
prod_price = st.sidebar.text_input("Price", placeholder="1000")
primary_kw = st.sidebar.text_input("Primary Keyword", placeholder="girls summer wear")

st.sidebar.markdown("---")
target_size = st.sidebar.selectbox(
    "Select Image Size (px)",
    options=[800, 1000, 1200],
    index=1,
    help="1000px is recommended for WooCommerce."
)

# --- MAIN AREA: IMAGE UPLOADER ---
uploaded_files = st.file_uploader("Upload Product Images", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if uploaded_files:
    st.subheader("🖼️ Processed Images")
    cols = st.columns(4) # Show 4 images per row
    
    zip_buffer = io.BytesIO()
    processed_images = []

    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for idx, uploaded_file in enumerate(uploaded_files):
            # Open and Process Image
            img = Image.open(uploaded_file).convert("RGB")
            
            # Create white canvas
            new_img = Image.new("RGB", (target_size, target_size), (255, 255, 255))
            img.thumbnail((target_size, target_size))
            offset = ((target_size - img.size[0]) // 2, (target_size - img.size[1]) // 2)
            new_img.paste(img, offset)
            
            # Save to Buffer (Memory)
            img_io = io.BytesIO()
            new_img.save(img_io, "WEBP", quality=85)
            img_bytes = img_io.getvalue()
            
            # Add to ZIP
            file_name = f"{uploaded_file.name.split('.')[0]}.webp"
            zip_file.writestr(file_name, img_bytes)
            
            # Display in App
            with cols[idx % 4]:
                st.image(img_bytes, caption=file_name)
                st.download_button(
                    label="Download",
                    data=img_bytes,
                    file_name=file_name,
                    mime="image/webp",
                    key=f"btn_{idx}"
                )

    st.markdown("---")
    
    # --- DOWNLOAD ALL BUTTON ---
    st.download_button(
        label="📦 Download All as ZIP",
        data=zip_buffer.getvalue(),
        file_name=f"products_{datetime.now().strftime('%H%M%S')}.zip",
        mime="application/zip",
        use_container_width=True
    )

    # --- GEMINI PROMPT GENERATION ---
    st.subheader("📝 Gemini Instruction")
    st.info("Copy the text below and paste it into your Gemini Gem to generate your content.")
    
    gemini_prompt = f"""
    GENERATE CONTENT FOR:
    - Product: {prod_name}
    - Fabric: {prod_fabric}
    - Age: {prod_age}
    - Price: {prod_price}
    - Keyword: {primary_kw}
    
    REQUIREMENTS:
    1. SEO Slug, Meta Title (60 chars), Meta Description (160 chars)
    2. Size Chart Table (Age wise)
    3. Short Description & 600-word Blog (H1/H2 headings)
    4. 10 WooCommerce Tags & 3 FAQ Section
    
    STYLE: Use the writing style from my attached NotebookLM books.
    """
    st.code(gemini_prompt, language="text")

else:
    st.warning("Please upload images to begin.")