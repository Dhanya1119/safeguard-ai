# 🛡️ SafeGuard AI (Prototype)

### 🚨 Problem Statement
With the increase in internet usage, children and families are exposed to explicit/unsafe content involuntarily. Most platforms fail to block sensitive content effectively in real-time.

### 💡 The Solution: SafeGuard AI
SafeGuard AI is an intelligent content filtering prototype that detects Nudity and Sensitive content using Advanced Computer Vision.

**Strict Mode:** Unlike standard filters, this AI protects users even from borderline explicit content (like Swimwear/Bikini) to ensure 100% Indian Cultural Safety standards.

### 🚀 Key Features
- **Strict Logic:** Blocks content even with 20% NSFW confidence.
- **Privacy First:** Images are processed and blurred instantly.
- **Smart Blur:** Visual blurring instead of just deleting content.
- **Deployment:** Live on Streamlit Cloud.

### 🛠️ Tech Stack
- **Language:** Python
- **Interface:** Streamlit
- **AI Model:** HuggingFace Transformers (AdamCodd/vit-base-nsfw-detector)
- **Image Processing:** Pillow (PIL)

### 🔮 Future Roadmap (The Vision)
This web app is a **Proof of Concept (PoC)**.
The final goal is to build an **Android System-Level Service** that runs in the background and blocks explicit content across ALL apps (Instagram, Chrome, Twitter, etc.) in real-time.

---
*Built by Dhanya (1st Year CSE) for Scaler School of Technology Hackathon.*
