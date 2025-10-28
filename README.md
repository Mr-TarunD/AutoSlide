# AutoSlide 📄➡️📊

Instantly convert text-based PDFs or raw text into summary bullet points and export them as a PowerPoint (.pptx) presentation.

![AutoSlide Screenshot](https://via.placeholder.com/800x400.png?text=Add+App+Screenshot+Here)
*<(Add a screenshot or GIF of your running application here!)*

---

## 🚀 Features

* **📄 PDF Upload:** Process any text-based PDF document.
* **📋 Text Paste:** Directly paste raw text into the app for summarization.
* **🤖 Dual Summarization Modes:**
    * **AI Mode (Abstractive):** Uses the `facebook/bart-large-cnn` Transformer model for high-quality, human-like summaries.
    * **Fast Mode (Extractive):** Uses `sumy`'s TextRank algorithm for a lightweight and speedy summary.
* **🎚️ Adjustable Length:** Use a simple slider to control the conciseness of the generated summary.
* **📊 PowerPoint Export:** Download your generated bullet points as a fully-formatted `.pptx` file with a title slide and content slides.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **Backend:** [Python 3](https://www.python.org/)
* **PDF Reading:** [pdfplumber](https://github.com/jsvine/pdfplumber)
* **AI Summarization:** [Hugging Face `transformers`](https://huggingface.co/docs/transformers/index)
* **Extractive Summarization:** [sumy](https://github.com/miso-belica/sumy)
* **PowerPoint Generation:** [python-pptx](https://python-pptx.readthedocs.io/en/latest/)

---

## ⚙️ Getting Started

Follow these instructions to get the project running on your local machine.

### 1. Prerequisites

* [Python 3.8+](https://www.python.org/downloads/)
* `git` (for cloning the repo)

### 2. Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/autoslide.git](https://github.com/your-username/autoslide.git)
    cd autoslide
    ```

2.  **Create and activate a virtual environment:**
    * On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Run the App

1.  **Launch the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
2.  Your default web browser will automatically open with the app.

    > **Note:** The first time you run the app using the **AI Mode** (with "Fast mode" unchecked), it will download the `bart-large-cnn` model (approx. 1.6 GB). This is a one-time process.

---

## 🕹️ How to Use

1.  Once the app is running, choose your input method:
    * **📄 Upload PDF:** Drag and drop or browse for a PDF file.
    * **📋 Paste Text:** Click the tab and paste your text into the text area.
2.  In the sidebar, configure your summary:
    * Check **"Use fast mode"** for a quick extractive summary.
    * Uncheck it to use the more powerful (but slower) AI model.
    * Adjust the **"Summary Conciseness"** slider. (Lower = shorter summary).
3.  Click the **"Generate Points"** button.
4.  Review your generated bullet points in the main area.
5.  Click the **"Download PowerPoint (.pptx)"** button to save your presentation.

---

## 🔧 Troubleshooting

* **Error: `streamlit: command not found`**
    * **Cause:** Your virtual environment (`venv`) is not activated.
    * **Fix:** Run `.\venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux). If that fails, run the app using `python -m streamlit run app.py`.

* **Error: `ModuleNotFoundError: No module named 'transformers'` (or any other module)**
    * **Cause:** Packages were not installed correctly.
    * **Fix:** Ensure your `venv` is active and run `pip install -r requirements.txt`.

* **Error: `Extractive summarization failed`**
    * **Cause:** This happens in "Fast mode" if the input text is too short, too simple, or in a language other than English.
    * **Fix:** Try **unchecking "Use fast mode"** to use the AI model, which is much more robust.

* **Error: `ConnectionError: HUGGINGFACE_CO...` (during first AI run)**
    * **Cause:** No internet connection, or a firewall is blocking the download of the Transformer model.
    * **Fix:** Check your internet connection. If on a corporate network, use "Fast mode" or try again on a different network.

* **App is very slow, freezes, or crashes in AI mode:**
    * **Cause:** Out of Memory (OOM). The AI model is large.
    * **Fix:** Your computer may not have enough RAM. Use **"Use fast mode"** or try processing a smaller document.

---

