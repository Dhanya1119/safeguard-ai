import streamlit as st
from transformers import pipeline
from PIL import Image, ImageFilter

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="SafeGuard AI", page_icon="🛡️", layout="centered")

# --- 2. ADVANCED CSS (NEON THEME KEPT AS IT IS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    /* BACKGROUND */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #002B5B 0%, #021a35 40%, #000000 100%);
        color: white;
        font-family: 'Roboto', sans-serif;
    }

    /* HEADER & LOGO */
    .logo-box {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 198, 255, 0.1));
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(0, 255, 136, 0.3);
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.2);
        backdrop-filter: blur(5px);
    }
    .shield-icon { font-size: 60px; margin-right: 15px; text-shadow: 0 0 20px #00ff88; }
    .logo-text {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 45px;
        text-transform: uppercase;
        background: linear-gradient(to right, #00c6ff, #0072ff, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 10px rgba(0, 198, 255, 0.5));
    }
    .logo-sub {
        font-size: 12px;
        color: #aaa;
        letter-spacing: 2px;
        font-family: 'Orbitron';
    }

    /* UPLOAD BOX - NEON GREEN VISIBILITY */
    [data-testid="stFileUploaderDropzone"] {
        background-color: rgba(0, 0, 0, 0.8) !important;
        border: 2px dashed #00ff88 !important;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
    }
    [data-testid="stFileUploaderDropzone"] div,
    [data-testid="stFileUploaderDropzone"] span,
    [data-testid="stFileUploaderDropzone"] small,
    [data-testid="stFileUploaderDropzone"] label {
        color: #FFFFFF !important;
        font-weight: bold !important;
    }
    [data-testid="stFileUploaderDropzone"] button {
        background-color: rgba(0, 255, 136, 0.1) !important;
        border: 1px solid #00ff88 !important;
        color: #FFFFFF !important;
    }

    /* INSTRUCTION TEXT */
    .instruction-text {
        text-align: center;
        font-size: 20px;
        font-weight: 700;
        color: #00FFFF !important;
        margin-top: 10px;
        margin-bottom: 10px;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.4);
    }

    /* RESET BUTTON */
    .stButton>button {
        width: 100%;
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(90deg, #ff416c, #ff4b2b);
        border: none;
        color: white;
        font-weight: 900;
        font-size: 18px;
        padding: 12px;
        border-radius: 8px;
        box-shadow: 0 0 15px rgba(255, 75, 43, 0.5);
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 30px rgba(255, 75, 43, 0.8);
    }

    /* STATUS CARDS */
    .status-safe { 
        border: 2px solid #00ff88; 
        background: rgba(0, 255, 136, 0.1); 
        color: #00ff88; 
        padding: 20px; 
        border-radius: 15px; 
        text-align: center; 
        font-family: 'Orbitron', sans-serif; 
        font-size: 24px;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
    }
    .status-unsafe { 
        border: 2px solid #ff4b4b; 
        background: rgba(255, 75, 75, 0.1); 
        color: #ff4b4b; 
        padding: 20px; 
        border-radius: 15px; 
        text-align: center; 
        font-family: 'Orbitron', sans-serif; 
        font-size: 24px;
        box-shadow: 0 0 20px rgba(255, 75, 75, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
st.markdown("""
    <div class="logo-box">
        <span class="shield-icon">🛡️</span>
        <div style="display:flex; flex-direction:column;">
            <span class="logo-text">SAFEGUARD AI</span>
            <span class="logo-sub">INTELLIGENT PROTECTION PROTOCOL</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 4. LOAD AI ---
@st.cache_resource
def load_classifier():
    return pipeline("image-classification", model="AdamCodd/vit-base-nsfw-detector")

with st.spinner("🔄 SYSTEM INITIALIZING..."):
    classifier = load_classifier()

# --- 5. LOGIC (AUTOMATIC SCAN) ---

# Uploader Key for Reset functionality
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = str(0)

# Instruction
st.markdown('<p class="instruction-text">✨ Upload to Scan Automatically ✨</p>', unsafe_allow_html=True)

# UPLOAD BOX
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], key=st.session_state.uploader_key)

# TRIGGER IMMEDIATELY IF FILE UPLOADED
if uploaded_file is not None:
    
    # Just show a quick spinner while processing
    with st.spinner("⚡ AUTO-SCANNING PIXEL MATRIX..."):
        image = Image.open(uploaded_file)
        
        # 1. RUN AI
        results = classifier(image)
        
        # 2. GET SCORE
        nsfw_score = 0.0
        for item in results:
            if item['label'] == 'nsfw':
                nsfw_score = item['score']
                break
        
        # 3. DISPLAY RESULT IMMEDIATELY
        if nsfw_score > 0.2:
            # UNSAFE
            st.markdown('<div class="status-unsafe">🚫 BLOCKED (STRICT MODE)</div>', unsafe_allow_html=True)
            
            # BLUR Logic
            blurred_img = image.filter(ImageFilter.GaussianBlur(radius=60))
            st.image(blurred_img, caption="Content Blurred for Safety", use_column_width=True)
            
        else:
            # SAFE
            st.markdown('<div class="status-safe">✅ SAFE TO VIEW</div>', unsafe_allow_html=True)
            
            # ORIGINAL Image
            st.image(image, caption="Verified Safe Content", use_column_width=True)

    # 4. RESET BUTTON (To Clear and Upload New)
    st.write("") # small gap
    if st.button("🔄 SCAN NEW FILE"):
        # Just update the key to reset the uploader
        st.session_state.uploader_key = str(int(st.session_state.uploader_key) + 1)
        st.rerun()
