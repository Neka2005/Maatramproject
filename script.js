const backend_url = "http://127.0.0.1:8000";

async function analyzeText() {
    const text = document.getElementById("textInput").value;
    if (!text) { alert("Enter text!"); return; }

    const response = await fetch(${backend_url}/analyze-text, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text})
    });

    const result = await response.json();
    document.getElementById("textResult").innerText =
        Sentiment: ${result.sentiment}\nConfidence: ${result.confidence}\nVerification: ${result.verification_status};
}

async function analyzeVoice() {
    const fileInput = document.getElementById("voiceInput");
    if (!fileInput.files.length) { alert("Upload voice file"); return; }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const response = await fetch(${backend_url}/analyze-voice, {
        method: "POST",
        body: formData
    });

    const result = await response.json();
    if (result.error) {
        document.getElementById("voiceResult").innerText = result.error;
    } else {
        document.getElementById("voiceResult").innerText =
        Text: ${result.text}\nSentiment: ${result.sentiment}\nConfidence: ${result.confidence}\nVerification: ${result.verification_status};
    }
}