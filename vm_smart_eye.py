import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="VM Smart Eye - AI Retail Agent",
    page_icon="👁️",
    layout="centered"
)

# --- Title and Introduction ---
st.title("👁️ VM Smart Eye")
st.markdown("### AI-Powered Retail Compliance Agent")
st.caption("Upload store photos, and the AI will automatically generate a compliance audit report based on VM guidelines.")

# --- Sidebar: API Key Settings ---
with st.sidebar:
    st.header("⚙️ Settings")
    # Try to load API Key from Streamlit Secrets first
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("API Key loaded from system ✅")
    else:
        api_key = st.text_input("Enter Google API Key", type="password")
        st.info("Please enter your Gemini API Key to start.")
    
    st.markdown("---")
    st.markdown("**About this Project**")
    st.markdown("Agents Intensive Capstone Project.")
    st.markdown("Author: Noel Chan")

# --- Main Interface ---

# 1. VM Guidelines Input (Default: 2025 Spring Collection)
default_guidelines = """【2025 Spring Collection Visual Guidelines】

1. **Color Palette:**
Key colors: "Sage Green" and "Pistachio".
Must display a "Monochromatic" layered look.

2. **Window Display:**
Must include the "2025 Spring Collection" Decal, placed centered.
Glass must be clean and free of fingerprints.

3. **Mannequin Styling:**
Mannequins must wear the key green collection items.
Use the "Relaxed Logic" pose to showcase natural drape.

4. **Housekeeping:**
Pantone Floor Decal must be clearly visible and undamaged.
Rails must be level, and hanger spacing should be 2 fingers wide."""

with st.expander("📝 View or Modify VM Guidelines", expanded=False):
    guideline_text = st.text_area("Current Guidelines", value=default_guidelines, height=200)

# 2. Photo Upload
uploaded_file = st.file_uploader("📸 Upload Store Display Photo", type=["jpg", "jpeg", "png"])

# --- Core Logic ---
if uploaded_file is not None and api_key:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Photo", use_column_width=True)

    # Analysis Button
    if st.button("🔍 Start Audit", type="primary"):
        try:
            # Configure API
            genai.configure(api_key=api_key)
            
            # Prepare Prompt (Based on your original logic)
            sys_instruction = """You are "VM Smart Eye," a Senior Visual Merchandising Manager.
            Your Goal: Analyze store photos for compliance with brand guidelines.
            Your Tone: Professional, constructive, and detail-oriented."""

            prompt = f"""
            You are a Senior Visual Merchandising Manager (VM Smart Eye) with 15 years of experience.
            Your task is to review the store display photo for compliance with the current season's Guidelines.

            Current Guidelines:
            {guideline_text}

            Please perform the following steps:
            1. **Visual Analysis and Report Generation**:
            Carefully observe the image, compare it against the guidelines, and generate a professional compliance report IN ENGLISH.

            The report format must be Markdown:

            ## 👁️ VM Smart Eye Smart Audit Report
            **📊 Compliance Score:** [0-10] / 10
            **✅ Highlights:** ...
            **⚠️ Non-Compliance & Improvement Suggestions:** ...
            **💡 Expert Insights:** ...
            """

            # Call Model (Using Gemini 2.0 Flash or 1.5 Flash)
            with st.spinner('VM Smart Eye is performing visual analysis... (This may take a few seconds)'):
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash-001", # Switch to "gemini-1.5-flash" if 2.0 is unavailable
                    system_instruction=sys_instruction
                )
                
                response = model.generate_content([prompt, image])
                report_content = response.text

            # Display Result
            st.success("Analysis Complete!")
            st.markdown("---")
            st.markdown(report_content)

            # Download Button
            st.download_button(
                label="📥 Download Report (Markdown)",
                data=report_content,
                file_name="vm_audit_report.md",
                mime="text/markdown"
            )

            # Feedback UI
            st.markdown("---")
            st.subheader("💬 Rate this result")
            feedback = st.feedback("stars")
            if feedback is not None:
                st.write("Thank you for your feedback!")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.warning("Please check your API Key or verify if the model version is currently available.")

elif not api_key:
    st.warning("👈 Please enter your Google API Key in the sidebar first.")
