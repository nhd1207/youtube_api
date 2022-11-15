# Text CNN 
import pandas as pd 
import numpy as np 
import re
import pickle

import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt

import tensorflow as tf
from keras.layers import Input, Dense, Embedding, Conv2D, MaxPool2D
from keras.layers import Reshape, Flatten, Dropout, Concatenate
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam
from keras.models import Model
from keras.utils import to_categorical, pad_sequences
from keras.preprocessing import text, sequence

from sklearn.metrics import f1_score, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit


MODEL_FILE = './model/Text_CNN_model_v13.h5'

import tensorflow as tf
from tensorflow import keras

text_model = keras.models.load_model('./model/Text_CNN_model_v13.h5')
text_model.summary()

# ## LOAD TOKENIZER

def pre_process_features(X, y, tokenized = True, lowercased = True):

    X = [preprocess(str(p), tokenized = tokenized, lowercased = lowercased) for p in list(X)]

    for idx, ele in enumerate(X):

        if not ele:

            np.delete(X, idx)

            np.delete(y, idx)

    return X, y

EMBEDDING_FILE = './cc.vi.300.vec'
MODEL_FILE = './model/Text_CNN_model_v13.h5'


# ## LOAD TOKENIZER

# In[6]:


def make_featues(X, y, tokenizer, is_one_hot_label=True):
    X = tokenizer.texts_to_sequences(X)
    X = pad_sequences(X, maxlen=sequence_length)
    if is_one_hot_label: 
        y = to_categorical(y, num_classes=3)

    return X, y


# In[7]:


vocabulary_size = 10000
sequence_length = 100

embedding_dim = 300
batch_size = 256
epochs = 40
drop = 0.5

filter_sizes = [2,3,5]
num_filters = 32


# In[8]:

def LoadTokenzier(file_path):
    with open(file_path, 'rb') as f:
        # unpickler = pickle.Unpickler(f)
        # tokenizer = unpickler.load()
        tokenizer = pickle.load(f)
    return tokenizer

tokenzier_path = './tokenizer.pickle'
tokenizer = LoadTokenzier(tokenzier_path)


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


from flask import Flask, request

app = Flask(__name__)

@app.get("/")
def predict():
    app.logging.info("predicting...")
    blob_url = request.args.get('blob_url')
    # In[ ]:

    data_file = pd.read_csv(blob_url, on_bad_lines='skip')

    youtube_url = data_file["youtube_url"][0]
    blink_data = data_file['content']



    tet_pre = pre_process_features(blink_data)

    test_thu = EncodeSentence(tet_pre,tokenizer)

    tet_pre


    # In[19]:


    label = {0:"clean", 1:"offensive", 2:"hate"}
    response = {
        "success": True,
        "result": []
    }
    # f = open(f"output/predict_result.csv", "w")
    # f.write("youtube_url,content,label_id\n")


    for index in range(len(blink_data)):

    #   print(blink_data[index])
        content = blink_data[index]

    #   print(label[(text_model.predict(test_thu).argmax(axis=-1)[index])])
        signed_label = label[(text_model.predict(test_thu).argmax(axis=-1)[index])]
        # f.write(f"{youtube_url},{content},{signed_label}\n")
        response["result"].append({"content": content, "label": signed_label})
    
    app.logging.info("done predicting.")
    return response

    # f.close()
