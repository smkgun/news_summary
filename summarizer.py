# 파이어: summarizer.py
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

def summarize_text(text, lead='', sentence_count=3):
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("korean"))
        summarizer = TextRankSummarizer()
        summary = summarizer(parser.document, sentence_count)
        body = " ".join([str(sentence) for sentence in summary])
        return f"{body}" if lead in body else f"{lead}\n\n{body}"
    except:
        return (lead + "\n\n" if lead else "") + text[:300] + " ..."
