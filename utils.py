import re
import stanza
import nltk
from collections import Counter
import pandas as pd
import streamlit as st

nltk.download('stopwords')
stanza.download('pt')

@st.cache_resource(show_spinner="Carregando seus resultados")
class CreateTokens:
    def __init__(self, text: str):
        self.text = text
        self.nlp = stanza.Pipeline('pt', processors='tokenize,mwt,pos,lemma', quiet=True)
        self.stopwords = set(nltk.corpus.stopwords.words('portuguese'))
        self.words = self.process_text()

    def __str__(self):
        return ' '.join(self.words)

    def __repr__(self):
        return f"CreateTokens(words={self.words})"

    def limpa_pontuacao(self, text: str) -> str:
        return re.sub(r'[^\w\s]', '', text)

    def lemmatiza_texto(self, text: str) -> list:
        doc = self.nlp(text)
        lemmatized_words = []

        for sentence in doc.sentences:
            for word in sentence.words:
                lemmatized_words.append(word.lemma)

        return lemmatized_words

    def remove_stopwords(self, words: list) -> list:
        return [word for word in words if word.lower() not in self.stopwords]
    
    def process_text(self) -> list:
        texto_limpo = self.limpa_pontuacao(self.text)
        palavras_lematizadas = self.lemmatiza_texto(texto_limpo)
        palavras_final = self.remove_stopwords(palavras_lematizadas)
        return palavras_final

    def get_words(self) -> list:
        return self.words

class TokenCounter:
    def __init__(self, stored_tokens: list):
        self.stored_tokens = set(stored_tokens)

    def count_tokens_in_text(self, tokens: list) -> dict:
        token_counts = Counter()
        for word in tokens:
            if word in self.stored_tokens:
                token_counts[word] += 1
        return dict(token_counts)
    
class retrieveTopTen:
    def __init__(self, retrieved: list):
        self.retrieved = sorted(pd.DataFrame(retrieved))
        organizados = self.retrieved
        return pd.DataFrame(organizados).nlargest(5,keep='all')