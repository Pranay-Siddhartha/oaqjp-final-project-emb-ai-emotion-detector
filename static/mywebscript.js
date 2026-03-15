let RunSentimentAnalysis = () => {
    const textToAnalyze = document.getElementById("textToAnalyze").value;
    const output = document.getElementById("system_response");

    if (!textToAnalyze.trim()) {
        output.innerHTML = "<span style='color: #c00;'>Please enter some text.</span>";
        return;
    }

    output.innerHTML = "<em>Detecting emotion...</em>";

    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState !== 4) return;

        if (this.status === 200) {
            output.innerHTML = this.responseText;
        } else {
            output.innerHTML = `<span style='color: #c00;'>Error (${this.status}): ${this.responseText}</span>`;
        }
    };

    xhttp.onerror = () => {
        output.innerHTML = "<span style='color: #c00;'>Network error. Is the server running?</span>";
    };

    const encoded = encodeURIComponent(textToAnalyze);
    xhttp.open("GET", `/emotionDetector?textToAnalyze=${encoded}`, true);
    xhttp.send();
};
