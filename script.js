const summarizeBtn = document.getElementById("summarizeBtn");
const askBtn = document.getElementById("askBtn");

const videoUrl = document.getElementById("videoUrl");
const questionInput = document.getElementById("questionInput");

const summaryBox = document.getElementById("summaryBox");
const answerBox = document.getElementById("answerBox");

const loading = document.getElementById("loading");

function showLoading() {
    loading.style.display = "block";
}

function hideLoading() {
    loading.style.display = "none";
}

summarizeBtn.addEventListener("click", async () => {

    const url = videoUrl.value.trim();

    if (!url) {
        alert("Please enter a YouTube URL.");
        return;
    }

    showLoading();

    summaryBox.innerHTML = "Generating summary...";
    answerBox.innerHTML = "AI answers will appear here...";

    try {

        const response = await fetch("/summarize", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url: url
            })
        });

        const data = await response.json();

        summaryBox.innerText = data.summary;

    }

    catch (error) {

        summaryBox.innerText = "Something went wrong.";

        console.error(error);

    }

    hideLoading();

});



askBtn.addEventListener("click", async () => {

    const question = questionInput.value.trim();

    if (!question) {
        alert("Please enter a question.");
        return;
    }

    showLoading();

    answerBox.innerHTML = "Thinking...";

    try {

        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        answerBox.innerText = data.answer;

    }

    catch (error) {

        answerBox.innerText = "Something went wrong.";

        console.error(error);

    }

    hideLoading();

});