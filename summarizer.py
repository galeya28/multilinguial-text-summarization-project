from transformers import pipeline
from langdetect import detect
import pdfplumber
from newspaper import Article
import yake
from wordcloud import WordCloud

# Load multilingual summarization model
summarizer = pipeline(
    "summarization",
    model="csebuetnlp/mT5_multilingual_XLSum"
)

def detect_language(text):

    try:
        return detect(text)
    except:
        return "unknown"


def summarize_text(text):

    summary = summarizer(
        text,
        max_length=120,
        min_length=30,
        do_sample=False
    )

    return summary[0]['summary_text']


def extract_text_from_pdf(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:
            text += page.extract_text()

    return text


def extract_text_from_url(url):

    article = Article(url)
    article.download()
    article.parse()

    return article.text


def extract_keywords(text):

    kw_extractor = yake.KeywordExtractor()

    keywords = kw_extractor.extract_keywords(text)

    result = []

    for kw in keywords[:5]:
        result.append(kw[0])

    return result


def generate_wordcloud(text):

    wc = WordCloud(width=800, height=400).generate(text)

    wc.to_file("static/wordcloud.png")
