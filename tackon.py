import string
import warnings
import random
import time
import nltk
import _thread
from win10toast import ToastNotifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


warnings.filterwarnings("ignore")
f=open('datackon-bot.txt','r',errors = 'ignore')
raw=f.read()
raw=raw.lower()

sent_tokens = nltk.sent_tokenize(raw)
salam_input = ("halo","hai", "hallo","hi","salam","hei","hey","ay","heh","oy", "ay","sayang","tackon", "halo tackon","hai tackon","bot")
respon_salam = ["halo","hai", "hallo","hi","hei","hey","ay","oy", "ay","iya sayang","tackon disini","hai ada yang bisa tackon bantu?","*senyum* :)", "nggih?", "dalem"]
respon_bingung =["maksudnya?","maaf?", "saya gabisa jawab","hah? maaf?","apa? ucapkan dengan bahasa yang mudah dimengerti dong", "gangerti aku awakmu ngomong opo","tolong tanya dengan bahasa indonesia yang bisa dimengerti"]

def LemNormalize(text):
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    return [token for token in nltk.word_tokenize(text.lower().translate(remove_punct_dict))]

#ngerespon salam
def greeting(sentence):
    """jika usernya nyapa, bakal disapa juga"""
    for word in sentence.split():
        if word.lower() in salam_input:
            return random.choice(respon_salam)