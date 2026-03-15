"""EmotionDetection package.

This package provides a simple wrapper around emotion detection utilities.

It exposes a single function:

- `emotion_detector(text: str) -> str`

"""

from .emotion_detection import emotion_detector

__all__ = ["emotion_detector"]
