import os
import numpy as np
import tensorflow as tf
from transformers import BertTokenizer, TFBertModel
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string

import warnings

warnings.filterwarnings("ignore")

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

nltk.download('stopwords')
nltk.download('punkt')
ps = PorterStemmer()

model = tf.keras.models.load_model('HTML_Features_Analysis/models/P_tag_bert.h5', custom_objects={'TFBertModel': TFBertModel})
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased')


def encode_text(text, maxlen):
    input_ids = []
    attention_masks = []

    for row in text:
        encoded = tokenizer.encode_plus(
            row,
            add_special_tokens=True,
            max_length=maxlen,
            pad_to_max_length=True,
            return_attention_mask=True,
        )
        input_ids.append(encoded['input_ids'])
        attention_masks.append(encoded['attention_mask'])

    return np.array(input_ids, dtype=np.int32), np.array(attention_masks, dtype=np.int32)


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


# prediction function
def predict_sentiment(text):
    # # Preprocess the text
    transformed_text = transform_text(text)

    print("\n\n" + transformed_text)

    # Encode and pad the preprocessed text
    input_ids, attention_masks = encode_text([transform_text(text)], maxlen=64)

    # Make predictions
    predictions = model.predict([input_ids, attention_masks])

    # Get the predicted label
    label = np.argmax(predictions[0])

    return label

# text = 'this is legitimate content. please sign with gmail username and password in here'

# predicted_label = predict_sentiment(text)
# print("Predicted Label:", predicted_label)

# if predicted_label == 1:
#     print("\n\nApplication content looks like phishing")
# else:
#     print("\n\nLegitimate content")
