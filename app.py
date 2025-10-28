import streamlit as st
import io
from utils.pdf_reader import extract_text_from_pdf
from utils.summarizer import load_summarizer, summarize_with_model, summarize_extractive
from utils.ppt_creator import create_ppt

# --- Page Configuration ---
st.set_page_config(
    page_title="AutoSlide",
    page_icon="📄",
    layout="wide"
)

# --- Model Caching ---
@st.cache_resource
def get_summarizer():
    """
    Loads and caches the summarization model.
    Shows a notification to the user.
    """
    st.toast("Loading summarization model... (This can take a few minutes on first run)")
    try:
        model = load_summarizer(device="cpu")
        st.toast("Model loaded successfully!", icon="✅")
        return model
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        st.error("Please check your internet connection and 'transformers' installation.")
        return None

# --- Session State Initialization ---
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = None

# --- UI Layout ---
st.title("AutoSlide 📄➡️📊")
st.markdown("Convert any text-based PDF or pasted text into concise presentation bullet points.")

# --- Sidebar Controls ---
with st.sidebar:
    st.header("1. Configure Summary")
    use_fast_mode = st.checkbox(
        "Use fast mode (Extractive)", 
        value=False, 
        help="Faster, non-AI summary. Good for simple documents. Uncheck to use the 'bart-large-cnn' AI model."
    )
    
    summary_ratio = st.slider(
        "Summary Conciseness", 
        min_value=0.1, 
        max_value=0.8, 
        value=0.3, 
        step=0.05,
        help="Controls the length of the summary. Lower values = shorter summary."
    )
    
    st.header("2. Generate")
    generate_button = st.button("Generate Points", type="primary", use_container_width=True)

# --- Main App Logic (with Tabs for Input) ---
st.header("1. Choose Your Input")
tab1, tab2 = st.tabs(["📄 Upload PDF", "📋 Paste Text"])

with tab1:
    uploaded_file = st.file_uploader("Select a PDF file", type=["pdf"])
    
with tab2:
    pasted_text = st.text_area(
        "Paste your text here", 
        height=300, 
        placeholder="Paste the full text from your article, document, or notes here..."
    )

# This variable will hold the text to be summarized, regardless of source
text_to_process = None

if generate_button:
    st.session_state.summary = None # Reset summary on new generation
    
    # Step 1: Get Text (from tabs)
    with st.spinner("Step 1/2: Processing input..."):
        if pasted_text:
            st.info("Using pasted text as input.")
            text_to_process = pasted_text
        elif uploaded_file:
            st.info("Reading PDF as input.")
            try:
                text_to_process = extract_text_from_pdf(uploaded_file)
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
                st.stop()
        else:
            st.warning("Please upload a PDF or paste text to generate a summary.")
            st.stop()
        
        st.session_state.extracted_text = text_to_process # Save for the previewer
        st.success("Input processed successfully!")

    # Step 2: Generate Summary (if text was found)
    if text_to_process:
        with st.spinner("Step 2/2: Generating summary... (AI model can be slow)"):
            try:
                if use_fast_mode:
                    st.toast("Using fast mode (Sumy)...")
                    bullet_points = summarize_extractive(
                        text_to_process, 
                        ratio=summary_ratio
                    )
                else:
                    st.toast("Using AI model (transformers)...")
                    model = get_summarizer() # Get cached model
                    if model:
                        bullet_points = summarize_with_model(
                            text_to_process, 
                            model, 
                            ratio=summary_ratio
                        )
                    else:
                        st.error("AI model is not available. Cannot generate summary.")
                        st.stop()
                        
                st.session_state.summary = bullet_points
                st.success("Summary generated!")
                
            except Exception as e:
                st.error(f"Error during summarization: {e}")
                if not use_fast_mode:
                    st.warning("Hint: The AI model may have failed. Try 'fast mode' or a smaller document.")
                st.session_state.summary = None

# --- Display Results ---
if st.session_state.summary:
    st.header("2. Your Results")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Generated Bullet Points")
        st.markdown(st.session_state.summary)

        st.subheader("Export")
        try:
            with st.spinner("Creating PowerPoint..."):
                ppt_stream = create_ppt(st.session_state.summary)
            
            st.download_button(
                label="Download PowerPoint (.pptx)",
                data=ppt_stream,
                file_name="AutoSlide_Summary.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Failed to create PPTX: {e}")

    with col2:
        st.subheader("Original Text (Preview)")
        with st.expander("Click to see full input text"):
            st.text_area(
                "Input Text", 
                st.session_state.extracted_text, 
                height=400
            )