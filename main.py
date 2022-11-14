import tensorflow as tf
from tensorflow import keras

text_model = keras.models.load_model('./model/Text_CNN_model_v13.h5')
text_model.summary()


# In[ ]:


def LoadTokenzier(file_path):
    with open(file_path, 'rb') as f:
        # unpickler = pickle.Unpickler(f)
        # tokenizer = unpickler.load()
        tokenizer = pickle.load(f)
    return tokenizer

tokenzier_path = './tokenizer.pickle'
tokenizer1 = LoadTokenzier(tokenzier_path)


# In[ ]:


class EncodeInput: # Cái này tui code chơi thôi nếu đưa vô được OOP xong gọi ra thì tiện á
    def __init__(self, sentence):
        self.sentence = sentence

    def LoadStopWord(self):
        STOPWORDS = './data/vietnamese-stopwords-dash.txt'
        with open(STOPWORDS, "r") as ins:
            stopwords = []
            for line in ins:
                dd = line.strip('\n')
                stopwords.append(dd)
            stopwords = set(stopwords)

    def filter_stop_words(self, sentence, stop_words):
        new_sent = [word for word in self.sentence.split() if word not in stop_words]
        self.sentence = ' '.join(new_sent)
            
        return self.sentence

    def deEmojify(text):
        regrex_pattern = re.compile(pattern = "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            "]+", flags = re.UNICODE)
        return regrex_pattern.sub(r'',text)

    def preprocess(text, tokenized = True, lowercased = True):
        text = ViTokenizer.tokenize(text) if tokenized else text
        text = filter_stop_words(text, stopwords)
        text = deEmojify(text)
        text = text.lower() if lowercased else text
        return text

    # --------------TRICH XUAT DAC TRUNG -------------------------
    def pre_process_features(self, tokenized = True, lowercased = True):
        self.sentence = [preprocess(str(p), tokenized = tokenized, lowercased = lowercased) for p in list(self.sentence)]
        for idx, ele in enumerate(self.sentence):
            if not ele:
                np.delete(self.sentence, idx)
        return self.sentence
    
    def EncodeInput(self, tokenizer, sequence_length=100):
        X = tokenizer.texts_to_sequences(self.sentence)
        X = pad_sequences(self.sentence, maxlen=sequence_length)
        return X


# In[ ]:


from pyvi.ViTokenizer import ViTokenizer

STOPWORDS = './data/vietnamese-stopwords-dash.txt'
with open(STOPWORDS, "r") as ins:
    stopwords = []
    for line in ins:
        dd = line.strip('\n')
        stopwords.append(dd)
    stopwords = set(stopwords)

def filter_stop_words(train_sentences, stop_words):
    new_sent = [word for word in train_sentences.split() if word not in stop_words]
    train_sentences = ' '.join(new_sent)
        
    return train_sentences

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def preprocess(text, tokenized = True, lowercased = True):
    text = ViTokenizer.tokenize(text) if tokenized else text
    text = filter_stop_words(text, stopwords)
    text = deEmojify(text)
    text = text.lower() if lowercased else text
    return text

# --------------TRICH XUAT DAC TRUNG -------------------------
def pre_process_features(X, tokenized = True, lowercased = True):
    X = [preprocess(str(p), tokenized = tokenized, lowercased = lowercased) for p in list(X)]
    for idx, ele in enumerate(X):
        if not ele:
            np.delete(X, idx)
    return X


# In[17]:


def EncodeSentence(X, tokenizer, sequence_length=100):
    X = tokenizer.texts_to_sequences(X)
    X = pad_sequences(X, maxlen=sequence_length)
    return X


# In[18]:


tet = ['Người yêu của My cực kì xam lol']
tet_pre = pre_process_features(tet)
test_thu = EncodeSentence(tet_pre,tokenizer)
tet_pre


# In[ ]:

import pandas as pd 
import numpy as np 

data_file = pd.read_csv('https://nhdis402.blob.core.windows.net/data/youtube_url_2EnHPuNqjjA.csv', on_bad_lines='skip')

youtube_url = data_file["youtube_url"][0]
blink_data = data_file['content']



tet_pre = pre_process_features(blink_data)

test_thu = EncodeSentence(tet_pre,tokenizer)

tet_pre


# In[19]:


label = {0:"clean", 1:"offensive", 2:"hate"}
f = open(f"output/predict_result.csv", "w")
f.write("youtube_url,content,label_id\n")

for index in range(len(blink_data)):

#   print(blink_data[index])
    content = blink_data[index]

#   print(label[(text_model.predict(test_thu).argmax(axis=-1)[index])])
    signed_label = label[(text_model.predict(test_thu).argmax(axis=-1)[index])]
    f.write(f"{youtube_url},{content},{signed_label}\n")

f.close()