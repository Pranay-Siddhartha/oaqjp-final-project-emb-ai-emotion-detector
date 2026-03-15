import os

import pytest

from EmotionDetection import emotion_detector


@pytest.fixture(autouse=True)
def set_dry_run_env(monkeypatch):
    """Force deterministic behavior for unit tests."""
    monkeypatch.setenv("EMOTION_DETECTION_DRY_RUN", "1")


def test_emotion_detector_returns_label():
    # When dry-run mode is enabled, we should receive the predictable "neutral" label.
    label = emotion_detector("I am so happy today!")

    assert label == "neutral"


def test_emotion_detector_handles_empty_text():
    label = emotion_detector("")
    assert label == "neutral"
