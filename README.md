# Emotion Detector (Final Project)

This repository contains a simple web application that performs **emotion detection** on user-provided text.

The application supports two backends:

- **IBM Watson Natural Language Understanding** (if credentials are configured)
- **Hugging Face Transformers** as a fallback

## Running locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the web server:

```bash
python server.py
```

3. Open your browser at:

```
http://localhost:5000
```

## Testing

Run the unit tests with:

```bash
python -m pytest -q
```

## Notes

- To use IBM Watson NLU, set the environment variables `WATSON_APIKEY` and `WATSON_URL`.
- For deterministic tests, the code supports `EMOTION_DETECTION_DRY_RUN=1`.
