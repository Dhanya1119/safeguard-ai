import streamlit as st
from transformers import pipeline
from PIL import Image, ImageFilter

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="SafeGuard AI", page_icon="🛡️", layout="centered")

# --- 2. ADVANCED CSS (VISIBILITY FIXED) ---
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

    /* MOBILE RESPONSIVE */
    @media only screen and (max-width: 600px) {
        .logo-box { flex-direction: column; padding: 15px; }
        .shield-icon { font-size: 40px; margin-right: 0; margin-bottom: 5px; }
        .logo-text { font-size: 28px !important; text-align: center; }
        .logo-sub { text-align: center; font-size: 10px; }
    }

    /* --- UPLOAD BOX VISIBILITY FIX (NUCLEAR OPTION) --- */
    
    /* 1. Main Dropzone Area - Darker Background */
    [data-testid="stFileUploaderDropzone"] {
        background-color: rgba(0, 0, 0, 0.8) !important;
        border: 2px dashed #00c6ff;
        border-radius: 15px;
        padding: 30px; 
    }

    /* 2. INSTRUCTIONS TEXT (Drag and drop file here) */
    [data-testid="stFileUploaderDropzoneInstructions"] > div:first-child {
        color: #FFFFFF !important; /* Pure White */
        font-size: 18px !important;
        font-weight: bold !important;
        font-family: 'Roboto', sans-serif;
    }

    /* 3. SMALL TEXT (Limit 200MB) */
    [data-testid="stFileUploaderDropzoneInstructions"] > div:nth-child(2) small {
        color: #CCCCCC !important; /* Light Grey */
        font-size: 12px !important;
    }

    /* 4. THE BROWSE FILES BUTTON (CRITICAL FIX) */
    [data-testid="stFileUploaderDropzone"] button {
        background-color: rgba(255, 255, 255, 0.1) !important; /* Slight White BG */
        border: 1px solid #00c6ff !important; /* Cyan Border */
        color: #FFFFFF !important; /* White Text */
        font-weight: 700 !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }

    /* 5. Button Hover Effect */
    [data-testid="stFileUploaderDropzone"] button:hover {
        background-color: #00c6ff !important; /* Cyan BG */
        color: #000000 !important; /* Black Text */
        border-color: #00ff88 !important;
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.6) !important;
    }

    /* TEXT INSTRUCTION ABOVE BOX */
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

    /* MAIN ACTION BUTTONS */
    .stButton>button {
        width: 100%;
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(90deg, #00c6ff, #00ff88);
        border: none;
        color: #002333;
        font-weight: 900;
        font-size: 20px;
        padding: 16px;
        border-radius: 8px;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 40px rgba(0, 198, 255, 0.8);
        color: white;
    }

    /* STATUS CARDS */
    .status-safe { border: 2px solid #00ff88; background: rgba(0, 255, 136, 0.1); color: #00ff88; padding: 15px; border-radius: 10px; text-align: center; font-family: 'Orbitron'; font-size: 22px; }
    .status-unsafe { border: 2px solid #ff4b4b; background: rgba(255, 75, 75, 0.1); color: #ff4b4b; padding: 15px; border-radius: 10px; text-align: center; font-family: 'Orbitron'; font-size: 22px; }
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
st.markdown('<p class="instruction-text">✨ Check if your Image is Safe or Not ✨</p>', unsafe_allow_html=True)

# UPLOAD BOX
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], key=st.session_state.uploader_key)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # PREVIEW
    if not st.session_state.scanned:
        st.image(image, caption="Uploaded File (Ready to Scan)", use_column_width=True)

    # ACTION BUTTON
    if st.button("ACTIVATE SCAN"):
        with st.spinner("⚡ PROCESSING DATA MATRIX..."):
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
        st.markdown('<div class="status-unsafe">🚫 BLOCKED (STRICT MODE)</div>', unsafe_allow_html=True)
        st.image(st.session_state.final_img, caption="Content Blurred for Safety", use_column_width=True)
        
    elif st.session_state.status == "SAFE":
        st.markdown('<div class="status-safe">✅ SAFE TO VIEW</div>', unsafe_allow_html=True)
        st.image(st.session_state.final_img, caption="Verified Safe Content", use_column_width=True)
    
    # RESET
    if st.button("SCAN NEW FILE"):
        st.session_state.scanned = False
        st.session_state.final_img = None
        st.session_state.status = ""
        st.session_state.uploader_key = str(int(st.session_state.uploader_key) + 1)
        st.rerun()
