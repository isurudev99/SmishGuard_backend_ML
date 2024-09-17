from IPython.display import clear_output
import warnings
warnings.filterwarnings('ignore')
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModel
import re
import numpy as np
from transformers import BertTokenizer
# !pip install transformers

print("\n\nfile Accessed\n\n")

"""Load Default MobileBERT model"""
checkpoint = "google/mobilebert-uncased"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = TFAutoModel.from_pretrained(checkpoint, output_hidden_states=True)


# def tokenization(data, **kwargs):
#     return tokenizer(data,
#                    padding=kwargs.get('padding','longest'),
#                    max_length=kwargs.get('max_length',55),
#                    truncation=True,
#                    return_tensors="tf")


"""# Define a new model"""
def get_model(**kwargs):
    global model
    max_seq_length = kwargs.get('max_seq_length',55)

    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained('google/mobilebert-uncased')
    input_ids = tf.keras.Input(shape=(max_seq_length,), dtype='int32', name='input_ids')
    attention_mask = tf.keras.Input(shape=(max_seq_length,), dtype='int32', name='attention_mask')
    # Tokenize inputs and pass them through the MobileBERT model
    inputs = {'input_ids': input_ids, 'attention_mask': attention_mask}
    outputs = model(inputs)
    pooler_output = outputs['pooler_output']
    # Model Head
    h1 = tf.keras.layers.Dense(128, activation='relu')(pooler_output)
    dropout = tf.keras.layers.Dropout(0.2)(h1)
    output = tf.keras.layers.Dense(1, activation='sigmoid')(dropout)
    # Create and compile the new model
    new_model = tf.keras.models.Model(inputs=[input_ids, attention_mask], outputs=output)
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4)
    loss = tf.keras.losses.BinaryCrossentropy(from_logits=False)
    metrics = [tf.keras.metrics.BinaryAccuracy()]
    new_model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    return new_model

""" get object of a created model"""
new_model1 = get_model()

"""Load the model weights"""
new_model1.load_weights('SMS_classification/models/Final_sentiment_weights_MobileBert_final_new.h5')


def remove_URL(sentence):
    url_pattern = re.compile(r'https?://\S+|www\.\S+|bit\.ly/\S+|t\.co/\S+')
    modified_sentence = url_pattern.sub('', sentence)
    urls = url_pattern.findall(sentence)
    return modified_sentence, urls


def remove_numbers(sentence):
    sentence = ''.join([i for i in sentence if not i.isdigit()])
    return sentence

def remove_html(sentence):
    html=re.compile(r'<.*?>')
    return html.sub(r'',sentence)



# Load the tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

max_sequence_length = 55  # Set the desired sequence length

def tokenization(text):
    # Tokenize the text
    tokens = tokenizer.tokenize(text)

    # Convert tokens to input IDs
    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    # Pad or truncate the input IDs to the desired sequence length
    input_ids = input_ids[:max_sequence_length]
    padded_input_ids = input_ids + [0] * (max_sequence_length - len(input_ids))

    # Create attention mask
    attention_mask = [1] * len(input_ids) + [0] * (max_sequence_length - len(input_ids))

    # Convert the input IDs and attention mask to numpy arrays
    input_ids = np.array(padded_input_ids)
    attention_mask = np.array(attention_mask)

    return input_ids, attention_mask


"""*****PREDICTIONS*****"""

def test_result(text, model):
    text, url = remove_URL(text)
    input_ids, attention_mask = tokenization(text)
    result_proba = model.predict([np.array([input_ids]), np.array([attention_mask])])
    result = [1 if x > 0.5 else 0 for x in result_proba.ravel()]
    return result, url

#  call this function it will return the URLs availble as list and return prediction value
def predictions(text): 

    result, url = test_result(text, new_model1)

    # print("Predicted Label:", result)
    # print("Probabilities:", predictions)

    return result[0], url

# text = "This is a sample sentence with a URL: https://example.com and a short URL: bit.ly/12345"
# SMS_predict_label , url = predictions(text)
# print("SMS Precition it as: ", SMS_predict_label)
# print("URL is : ", url)

