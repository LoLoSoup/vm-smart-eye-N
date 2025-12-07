import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- 頁面設定 ---
st.set_page_config(
    page_title="VM Smart Eye - AI Retail Agent",
    page_icon="👁️",
    layout="centered"
)

# --- 標題與簡介 ---
st.title("👁️ VM Smart Eye")
st.markdown("### AI-Powered Retail Compliance Agent")
st.caption("上傳店鋪照片，AI 將根據 VM 指引自動生成合規審計報告。")

# --- 側邊欄：設定 API Key ---
with st.sidebar:
    st.header("⚙️ 設定")
    # 優先嘗試從 Streamlit Secrets 讀取 Key，如果沒有則讓用戶輸入
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("API Key 已從系統加載 ✅")
    else:
        api_key = st.text_input("輸入 Google API Key", type="password")
        st.info("請輸入您的 Gemini API Key 以開始使用。")
    
    st.markdown("---")
    st.markdown("**關於此專案**")
    st.markdown("Agents Intensive Capstone Project.")
    st.markdown("作者: Noel Chan")

# --- 主要功能區 ---

# 1. 輸入 VM 指引 (預設為 PDF 中的 2025 Spring Collection)
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

with st.expander("📝 檢視或修改 VM Guidelines (審計標準)", expanded=False):
    guideline_text = st.text_area("當前指引", value=default_guidelines, height=200)

# 2. 上傳照片
uploaded_file = st.file_uploader("📸 上傳店鋪陳列照片", type=["jpg", "jpeg", "png"])

# --- 核心邏輯 ---
if uploaded_file is not None and api_key:
    # 顯示預覽圖
    image = Image.open(uploaded_file)
    st.image(image, caption="已上傳的照片", use_column_width=True)

    # 按鈕開始分析
    if st.button("🔍 開始 AI 審計 (Start Audit)", type="primary"):
        try:
            # 設定 API
            genai.configure(api_key=api_key)
            
            # 準備 Prompt (來自你的 PDF)
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

            # 呼叫模型 (使用 Gemini 2.0 Flash 或 1.5 Flash)
            with st.spinner('VM Smart Eye 正在進行視覺分析... (這可能需要幾秒鐘)'):
                model = genai.GenerativeModel(
                    model_name="gemini-2.0-flash", # 如果 2.0 還未對所有人開放，可改為 gemini-1.5-flash
                    system_instruction=sys_instruction
                )
                
                response = model.generate_content([prompt, image])
                report_content = response.text

            # 顯示結果
            st.success("分析完成！")
            st.markdown("---")
            st.markdown(report_content)

            # 下載按鈕 (取代原本的 save_report_to_disk 工具)
            st.download_button(
                label="📥 下載報告 (Markdown)",
                data=report_content,
                file_name="vm_audit_report.md",
                mime="text/markdown"
            )

            # 簡單的收集回饋 UI
            st.markdown("---")
            st.subheader("💬 評價此結果")
            feedback = st.feedback("stars")
            if feedback is not None:
                st.write("感謝您的評價！")

        except Exception as e:
            st.error(f"發生錯誤: {e}")
            st.warning("請檢查您的 API Key 是否正確，或是模型版本是否可用。")

elif not api_key:
    st.warning("👈 請先在左側輸入 Google API Key")
