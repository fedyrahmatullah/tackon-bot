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
        
def response(responUser): 
    responTackon=''
    sent_tokens.append(responUser)
    if 'apa itu jti' in responUser or 'jurusan ti adalah' in responUser  or 'ti polije' in responUser or 'ti' in responUser:
        responTackon = responTackon+sent_tokens[0]
        return responTackon
    elif 'prayudisium' in responUser or 'khs' in responUser:
        responTackon = responTackon+sent_tokens[8]
        return responTackon

    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize)
    tfidf = TfidfVec.fit_transform(sent_tokens)
    
    vals = cosine_similarity(tfidf[-1], tfidf) 

    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2] 
    
    if(req_tfidf==0):
        responTackon=responTackon+"{}".format(random.choice(respon_bingung))
        return responTackon
    else:
        responTackon = responTackon+sent_tokens[idx]
        return responTackon

def reminder(event, angka, waktu, timer):
    while timer>0:
        time.sleep(1)
        timer-=1
    toaster = ToastNotifier()  
    toaster.show_toast("Pengingat", "Tuan, ini sudah {}.\nKegiatan Anda itu {}".format(angka+' '+waktu, ' '.join(event)), icon_path=None, duration=5)
    while toaster.notification_active(): time.sleep(0.1)

def main(responUser):
    if(responUser!='bye' or responUser!='dadah' or responUser!='mettu'):
        if(responUser=='terima kasih' or responUser=='thank you' or responUser=='thanks' or responUser=='suwun' or responUser=="makasih" ):
            global flag
            flag=False
            print("TACKON: sama-sama, selamat beraktifitas ya")
        else:
            if len(responUser)==0:
                print('TACKON:  {}'.format(random.choice(respon_bingung)))
            elif(greeting(responUser)!=None):
                print("TACKON: "+greeting(responUser))
            else:
                print("TACKON:", ''+response(responUser))
                sent_tokens.remove(responUser)
    else:
        flag=False


print("TACKON: Hai Namaku TACKON. Aku bakal bantu kamu ngejawab informasi yang kamu butuhin\n\
       sebagai mahasiswa TI Polije semester akhir oke?")
print('TACKON: Aku juga bisa membantumu dalam beberapa hal\n\
      yaitu ngingetin kamu, coba deh ketik "ingetin saya untuk [aktifitasmu] dalam [waktu] [menit atau jam]"\n\
      Kalau mau keluar, ketik bye atau dadah atau mettu ya!')
print('Pesan dari Fedy: TACKON ini ga sempurna guys,\n\
      jadi ada kemungkinan jawaban dia ganyambung sama pertanyaanmu jadi dimaklumi ya,\n\
      pastikan juga kamu tanya seputar kegiatan mahasiswa TI semester akhir ya <3')

flag=True
while(flag==True):
    responUser = input('->> ')
    responUser=responUser.lower()

    if 'ingetin saya untuk' in responUser:
        perintah=responUser.split()
        try:    
            if 'menit'==perintah[-1]:
                timer=int(perintah[-2])*60
            elif 'jam'==perintah[-1]:
                timer=int(perintah[-2])*3600
        except ValueError:
            print("TACKON: Jangan input angka desimal ya aku gatau guys :(")
            print("TACKON: inputin bilangan bulat, jangan desimal aku ga ngerti sayang")
            continue
        acara=perintah[3:-3]
        angka=perintah[-2]
        jenis_waktu=perintah[-1]
    
        print("TACKON: oke, tak ingetin buat {} dalam {} {}".format(' '.join(acara), angka, jenis_waktu))  
        _thread.start_new_thread(reminder,(acara, angka, jenis_waktu,timer)) 
    else:    
        main(responUser)

print("TACKON: Bye rek! sampai ketemu nanti, kalo butuh tackon panggil tackon lagi yaa <3") 
