async function analyze() {
    let dream = document.getElementById("dream").value;

    if (!dream.trim()) {
        alert("Please enter your dream!");
        return;
    }

    try {
        let res = await fetch("/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ dream })
        });

        let data = await res.json();

        let emotion = data.top_predictions ? .[0] ? .emotion || "Unknown";
        let meaning = data.meaning || "No meaning found.";

        document.getElementById("result").innerHTML = `
            <div class="result-box">
                <h3>🌙 Emotion: ${emotion}</h3>
                <p>${meaning}</p>
            </div>
        `;

    } catch (error) {
        console.error(error);

        document.getElementById("result").innerHTML = `
            <p style="color:red;">⚠ Error analyzing dream. Try again.</p>
        `;
    }
}