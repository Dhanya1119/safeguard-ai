import streamlit as st
from transformers import pipeline
from PIL import Image, ImageFilter

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="SafeGuard AI", page_icon="🛡️", layout="centered")

# --- 2. SIMPLE & CLEAN CSS ---
st.markdown("""
    <style>
    /* IMPORT FONTS: Aleo (for Headers) & Lato (for Body) - Simple & Clean */
    @import url('https://fonts.googleapis.com/css2?family=Aleo:wght@300;400;700&family=Lato:wght@300;400;700&display=swap');

    /* BACKGROUND */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #1a2a6c 0%, #b21f1f 100%, #fdbb2d 100%); /* Just kidding, sticking to Deep Blue/Black for contrast */
        background: radial-gradient(circle at 50% 10%, #002B5B 0%, #021a35 40%, #000000 100%);
        color: white;
        font-family: 'Lato', sans-serif; /* Body Text */
    }

    /* HEADER & LOGO */
    .logo-box {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
    }
    
    .shield-icon { font-size: 50px; margin-right: 15px; }
    
    .logo-text {
        font-family: 'Aleo', serif; /* Requested Font Style */
        font-weight: 700;
        font-size: 40px;
        letter-spacing: 1px;
        color: white;
        text-transform: uppercase;
    }
    
    .logo-sub {
        font-size: 14px;
        color: #ddd;
        font-family: 'Lato', sans-serif;
        letter-spacing: 1px;
    }

    /* --- UPLOAD BOX VISIBILITY FIX (WHITE TEXT) --- */
    
    section[data-testid="stFileUploaderDropzone"] {
        background-color: rgba(0, 0, 0, 0.5) !important;
        border: 2px dashed #a0a0a0;
        border-radius: 10px;
        padding: 40px 20px;
    }

    /* FORCE TEXT TO BE WHITE & SIMPLE */
    section[data-testid="stFileUploaderDropzone"] * {
        color: #FFFFFF !important; /* PURE WHITE */
        font-family: 'Aleo', serif !important;
        font-weight: 400 !important;
        font-size: 16px !important;
    }

    /* Browse Button Style */
    section[data-testid="stFileUploaderDropzone"] button {
        background-color: transparent;
        border: 1px solid white;
        color: white !important;
        border-radius: 5px;
    }

    /* Hover Effect */
    section[data-testid="stFileUploaderDropzone"]:hover {
        background-color: rgba(0, 0, 0, 0.7) !important;
        border-color: white;
    }

    /* INSTRUCTION TEXT */
    .instruction-text {
        text-align: center;
        font-size: 18px;
        font-family: 'Aleo', serif;
        color: #E0E0E0;
        margin-top: 15px;
        margin-bottom: 5px;
    }

    /* BUTTONS */
    .stButton>button {
        width: 100%;
        font-family: 'Aleo', serif;
        background: white;
        border: none;
        color: #002B5B;
        font-weight: 700;
        font-size: 18px;
        padding: 12px;
        border-radius: 5px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #f0f0f0;
        transform: scale(1.01);
    }

    /* STATUS CARDS */
    .status-safe { 
        border-left: 5px solid #00ff88; 
        background: rgba(0, 255, 136, 0.1); 
        color: white; 
        padding: 15px; 
        border-radius: 5px; 
        text-align: left; 
        font-family: 'Aleo', serif; 
    }
    .status-unsafe { 
        border-left: 5px solid #ff4b4b; 
        background: rgba(255, 75, 75, 0.1); 
        color: white; 
        padding: 15px; 
        border-radius: 5px; 
        text-align: left; 
        font-family: 'Aleo', serif; 
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
st.markdown("""
    <div class="logo-box">
        <span class="shield-icon">🛡️</span>
        <div style="display:flex; flex-direction:column;">
            <span class="logo-text">SafeGuard AI</span>
            <span class="logo-sub">Intelligent Content Protection</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 4. LOAD AI ---
@st.cache_resource
def load_classifier():
    return pipeline("image-classification", model="AdamCodd/vit-base-nsfw-detector")

with st.spinner("Wait... System is getting ready"):
    classifier = load_classifier()

# --- 5. LOGIC ---
if 'scanned' not in st.session_state:
    st.session_state.scanned = False
if 'final_img' not in st.session_state:
    st.session_state.final_img = None
if 'status' not in st.session_state:
    st.session_state.status = ""
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = str(0)

# Instruction
st.markdown('<p class="instruction-text">Check if your Image is Safe or Not</p>', unsafe_allow_html=True)

# UPLOAD BOX
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], key=st.session_state.uploader_key)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    if not st.session_state.scanned:
        st.image(image, caption="Uploaded File", use_column_width=True)

    if st.button("RUN SCAN"):
        with st.spinner("Processing..."):
            results = classifier(image)
            nsfw_score = 0.0
            for item in results:
                if item['label'] == 'nsfw':
                    nsfw_score = item['score']
                    break
            
            # STRICT LOGIC
            if nsfw_score > 0.2:
                st.session_state.status = "UNSAFE"
                st.session_state.final_img = image.filter(ImageFilter.GaussianBlur(radius=60))
            else:
                st.session_state.status = "SAFE"
                st.session_state.final_img = image
            
            st.session_state.scanned = True
            st.rerun()

# --- 6. RESULT ---
if st.session_state.scanned:
    
    if st.session_state.status == "UNSAFE":
        st.markdown("""
        <div class="status-unsafe">
            <h3>🚫 BLOCKED</h3>
            <p>Strict Mode: Content hidden for safety.</p>
        </div>
        """, unsafe_allow_html=True)
        st.image(st.session_state.final_img, caption="Blurred View", use_column_width=True)
        
    elif st.session_state.status == "SAFE":
        st.markdown("""
        <div class="status-safe">
            <h3>✅ SAFE</h3>
            <p>Content is verified and clean.</p>
        </div>
        """, unsafe_allow_html=True)
        st.image(st.session_state.final_img, caption="Original View", use_column_width=True)
    
    if st.button("SCAN NEW FILE"):
        st.session_state.scanned = False
        st.session_state.final_img = None
        st.session_state.status = ""
        st.session_state.uploader_key = str(int(st.session_state.uploader_key) + 1)
        st.rerun()
