# 파이어: summarizer.py
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

def summarize_text(text, lead='', sentence_count=4):
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("korean"))
        summarizer = TextRankSummarizer()
        summary = summarizer(parser.document, sentence_count)
        body = " ".join([str(sentence) for sentence in summary])
        return body.strip() if body else text[:500] + " ..."
    except:
        return text[:500] + " ..."
