from text_extract import extracted_text

import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer  # Latent Semantic Analysis

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

def summarize_text(text, sentence_count=3):
    # Preprocess the text using spaCy
    doc = nlp(text)
    processed_text = ' '.join([sent.text for sent in doc.sents])

    # Summarize using Sumy
    parser = PlaintextParser.from_string(processed_text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)

    return ' '.join([str(sentence) for sentence in summary])

# Example text
text = extracted_text
summary = summarize_text(text)
print("Summary:", summary)
