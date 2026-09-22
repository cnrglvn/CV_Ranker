# CV Ranker

Built as a self taught python project, this is a small tool that screens and ranks candidate CVs against a job description, using an LLM to score suitability and explain its reasoning.

## What it does

Upload a job description and a batch of candidate CVs (`.txt` files), and the app scores each candidate against the role, returning a ranked table with a match score (0–100) and a one-sentence explanation for each.

## How it works

The tool is written in Python. For each uploaded CV it sends a request to the Google Gemini API, which independently scores each candidate against the job description and returns a structured JSON output. The interface is Streamlit; a lightweight Python-to-web-app UI library that handles page information, file upload, and the results table. The model has built-in graceful error handling for API failure and malformed model output.

## Running it locally

1. Clone the repo and install dependencies:
```bash
   git clone https://github.com/cnrglvn/CV_Ranker.git
   cd CV_Ranker
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
```

2. Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

3. Create a `.env` file in the project root. In this file, write and save the line:
   GEMINI_API_KEY=<Your_API_Key> 

4. Run the app:
```bash
   streamlit run CV_Ranker.py
```
   This opens the app in your browser at `localhost:8501`.

## Notes

This tool was built as part of a project to learn python to a usable degree over the course of 2 weeks. The goal was a functioning, end-to-end tool, as opposed to a polished product. Scores are intended as a guide, not a decision.
