from flask import Flask, render_template, request
from summarizer import (
    summarize_text,
    detect_language,
    extract_text_from_pdf,
    extract_text_from_url,
    extract_keywords,
    generate_wordcloud
)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    summary = ""
    language = ""
    keywords = []

    if request.method == "POST":

        text = request.form.get("text")
        url = request.form.get("url")
        pdf_file = request.files.get("pdf")

        if url:
            text = extract_text_from_url(url)

        if pdf_file and pdf_file.filename != "":
            text = extract_text_from_pdf(pdf_file)

        if text:
            language = detect_language(text)
            summary = summarize_text(text)
            keywords = extract_keywords(text)
            generate_wordcloud(text)

    return render_template(
        "index.html",
        summary=summary,
        language=language,
        keywords=keywords
    )


if __name__ == "__main__":
    app.run(debug=True)
