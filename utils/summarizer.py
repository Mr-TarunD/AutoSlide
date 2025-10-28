from transformers import pipeline
import warnings

# Import Sumy components
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

# Note: We are replacing gensim with sumy, which is pure-Python
# and avoids the compilation errors.

def load_summarizer(model_name="facebook/bart-large-cnn", device="cpu"):
    """
    Loads the Hugging Face summarization pipeline.

    Args:
        model_name (str): The name of the model to load.
        device (str): "cpu" or "cuda" (if available).

    Returns:
        A transformers summarization pipeline object.
    """
    print(f"Loading summarization model '{model_name}' on {device}...")
    # Using device=-1 explicitly forces CPU for transformers pipeline
    device_num = 0 if device == "cuda" else -1
    try:
        summarizer = pipeline("summarization", model=model_name, device=device_num)
        print("Model loaded successfully.")
        return summarizer
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

def summarize_with_model(text, summarizer, ratio=0.3):
    """
    Summarizes text using the loaded transformers model.

    Args:
        text (str): The text to summarize.
        summarizer: The loaded pipeline object.
        ratio (float): The desired summary length as a ratio of the original.

    Returns:
        A string formatted as bullet points.
    """
    try:
        # Calculate target lengths based on ratio
        word_count = len(text.split())
        target_word_count = int(word_count * ratio)
        
        # Set sensible min/max lengths
        max_len = max(target_word_count, 60) # Ensure a reasonable max
        min_len = max(int(max_len * 0.5), 20) # Ensure a reasonable min
        
        # BART's max token limit is 1024. Truncation=True handles this.
        with warnings.catch_warnings():
            # Suppress "Your input sequence is longer..." warning
            warnings.simplefilter("ignore")
            summary_paragraph = summarizer(
                text, 
                max_length=max_len, 
                min_length=min_len, 
                do_sample=False,
                truncation=True
            )[0]['summary_text']
        
        # Format the single paragraph summary into bullet points
        bullet_points = [s.strip() for s in summary_paragraph.split('. ') if s.strip()]
        if not bullet_points:
            return "* Could not generate summary."
            
        return "\n".join([f"* {s}" for s in bullet_points])

    except Exception as e:
        print(f"Error during transformer summarization: {e}")
        return f"* Error in summarization: {e}"

def summarize_extractive(text, ratio=0.3):
    """
    Summarizes text using the sumy (extractive) summarizer (TextRank).

    Args:
        text (str): The text to summarize.
        ratio (float): The ratio of the summary (0.0 to 1.0).

    Returns:
        A string formatted as bullet points.
    """
    try:
        # Initialize the parser and tokenizer (using English)
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        
        # Initialize the summarizer
        stemmer = Stemmer("english")
        stop_words = get_stop_words("english")
        summarizer = TextRankSummarizer(stemmer)
        summarizer.stop_words = stop_words
        
        # Calculate number of sentences needed
        total_sentences = len(parser.document.sentences)
        num_sentences = max(1, int(total_sentences * ratio))

        # Get the summary
        summary_sentences = summarizer(parser.document, num_sentences)
        
        if not summary_sentences:
            return "* Could not generate summary (text may be too short or lack clear topics)."
            
        # Format as bullet points
        return "\n".join([f"* {str(s).strip()}" for s in summary_sentences if str(s).strip()])

    except Exception as e:
        print(f"Error during extractive summarization: {e}")
        return f"* Extractive summarization failed. Try a different document."