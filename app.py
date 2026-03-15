from flask import Flask, request, render_template

from EmotionDetection import emotion_detector


def create_app():

    app = Flask(__name__, template_folder="templates", static_folder="static")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/emotionDetector")
    def emotion_detector_endpoint():
        text_to_analyze = request.args.get("textToAnalyze", "")

        if not text_to_analyze:
            return "No text provided", 400

        try:
            detected = emotion_detector(text_to_analyze)
            return detected
        except Exception as e:
            return f"Error while detecting emotion: {e}", 500

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=True)
