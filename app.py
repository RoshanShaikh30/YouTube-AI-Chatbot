from flask import Flask, request, jsonify, send_from_directory
from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


app = Flask(__name__)

# Store transcript temporarily
current_transcript = ""


def get_video_id(url):

    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    elif "youtube.com/watch?v=" in url:
        return url.split("v=")[1].split("&")[0]

    return None


def get_transcript(video_id):

    transcript = YouTubeTranscriptApi().fetch(video_id)

    text = " ".join([entry.text for entry in transcript])

    return text


def summarize_video(transcript):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role":"system",
                "content":"You summarize YouTube videos."
            },

            {
                "role":"user",

                "content":f"""
Summarize this YouTube transcript.

Transcript:

{transcript}

Provide:

1. Main Topic

2. Key Points (bullet points)

3. Final Conclusion

Keep it concise.
"""
            }

        ]

    )

    return response.choices[0].message.content


def ask_question(transcript, question):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role":"system",
                "content":"Answer ONLY using the transcript. If the transcript doesn't contain the answer, say so."
            },

            {
                "role":"user",

                "content":f"""
Transcript:

{transcript}

Question:

{question}
"""
            }

        ]

    )

    return response.choices[0].message.content


@app.route("/")
def home():

    return send_from_directory(".", "frontend.html")

@app.route("/style.css")
def style():
    return send_from_directory(".", "style.css")


@app.route("/script.js")
def script():
    return send_from_directory(".", "script.js")


@app.route("/summarize", methods=["POST"])
def summarize():

    global current_transcript

    data = request.get_json()

    url = data["url"]

    video_id = get_video_id(url)

    current_transcript = get_transcript(video_id)

    summary = summarize_video(current_transcript)

    return jsonify({

        "summary": summary

    })


@app.route("/ask", methods=["POST"])
def ask():

    global current_transcript

    data = request.get_json()

    question = data["question"]

    answer = ask_question(current_transcript, question)

    return jsonify({

        "answer": answer

    })


if __name__ == "__main__":

    app.run(debug=True)