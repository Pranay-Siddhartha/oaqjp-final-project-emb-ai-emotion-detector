"""Emotion detection helpers.

This module supports two modes of operation:

- Watson NLP (if `WATSON_APIKEY` and `WATSON_URL` are set), using IBM Watson Natural
  Language Understanding to return an emotion label.
- Transformers fallback (in case Watson credentials are not available), using a
  small public model from Hugging Face.

The function is designed to be safe for unit testing and to avoid re-loading the
model on every call.
"""

import os
from typing import Optional

# The Watson SDK is optional. When it's not installed, we gracefully fall back.
try:
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from ibm_watson import NaturalLanguageUnderstandingV1
    from ibm_watson.natural_language_understanding_v1 import (
        EmotionOptions,
        Features,
    )
except ImportError:  # pragma: no cover
    NaturalLanguageUnderstandingV1 = None  # type: ignore

# Transformers is a lightweight fallback and is also optional.
try:
    from transformers import pipeline
except ImportError:  # pragma: no cover
    pipeline = None  # type: ignore


def _create_watson_nlu() -> Optional[NaturalLanguageUnderstandingV1]:
    """Create a Watson Natural Language Understanding client if credentials exist."""

    api_key = os.environ.get("WATSON_APIKEY") or os.environ.get("IBM_WATSON_APIKEY")
    service_url = os.environ.get("WATSON_URL") or os.environ.get("IBM_WATSON_URL")

    if not (api_key and service_url) or NaturalLanguageUnderstandingV1 is None:
        return None

    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(version="2021-08-01", authenticator=authenticator)
    nlu.set_service_url(service_url)
    return nlu


_watson_nlu = _create_watson_nlu()

# Load Hugging Face pipeline once to avoid re-downloading the model repeatedly.
_emotion_pipeline = None
if pipeline is not None:
    try:
        _emotion_pipeline = pipeline(
            "text-classification", model="j-hartmann/emotion-english-distilroberta-base"
        )
    except Exception:  # pragma: no cover
        _emotion_pipeline = None


def emotion_detector(text_to_analyze: str) -> str:
    """Detect the primary emotion in the given text.

    The returned value is the emotion label (e.g., 'joy', 'anger', 'sadness').

    Args:
        text_to_analyze: The text to analyze.

    Returns:
        A single emotion label string.
    """

    # Unit tests and isolated runs can set this to skip any external calls.
    if os.environ.get("EMOTION_DETECTION_DRY_RUN") == "1":
        return "neutral"

    # Prefer Watson when configuration is present.
    if _watson_nlu is not None:
        response = _watson_nlu.analyze(
            text=text_to_analyze,
            features=Features(emotion=EmotionOptions()),
        )
        # Watson returns the emotion scores in a dict; choose the strongest.
        emotion_scores = response.get_result().get("emotion", {}).get("document", {}).get("emotion", {})
        if emotion_scores:
            return max(emotion_scores.items(), key=lambda kv: kv[1])[0]

    # Fallback to transformers pipeline if available.
    if _emotion_pipeline is not None:
        result = _emotion_pipeline(text_to_analyze)
        if result and isinstance(result, list) and "label" in result[0]:
            return result[0]["label"]

    # If no model is available, raise a clear error.
    raise RuntimeError(
        "No emotion detection backend is available. Install 'ibm-watson' or 'transformers'."
    )
