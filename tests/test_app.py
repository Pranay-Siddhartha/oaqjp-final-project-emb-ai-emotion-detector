import os

import pytest

from app import create_app


@pytest.fixture(autouse=True)
def set_dry_run_env(monkeypatch):
    # Ensure endpoint returns a stable value during tests.
    monkeypatch.setenv("EMOTION_DETECTION_DRY_RUN", "1")


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()


def test_root_returns_html(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"NLP - Emotion Detection" in resp.data


def test_emotion_detector_endpoint_missing_text(client):
    resp = client.get("/emotionDetector")
    assert resp.status_code == 400


def test_emotion_detector_endpoint_returns_label(client):
    resp = client.get("/emotionDetector?textToAnalyze=I+love+this")
    assert resp.status_code == 200
    assert resp.data.decode("utf-8") == "neutral"
