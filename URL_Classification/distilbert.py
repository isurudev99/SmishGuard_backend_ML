import tensorflow as tf
from transformers import DistilBertTokenizer, TFDistilBertModel


# Load the tokenizer
dbert_tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

# Load the saved model from the .h5 file with the custom object scope
model = tf.keras.models.load_model(r'URL_Classification/models/1upgrade_trained_model.h5', custom_objects = {'TFDistilBertModel': TFDistilBertModel})

def predict_url(url):
    # Tokenize the URL
    inputs = dbert_tokenizer.encode_plus(url, add_special_tokens=True, max_length=32, padding='max_length', truncation=True)
    input_ids = tf.constant(inputs['input_ids'])[None, :]
    attention_mask = tf.constant(inputs['attention_mask'])[None, :]

    # Perform prediction
    prediction = model.predict([input_ids, attention_mask])[0]

    # Convert prediction to label
    label = 1 if prediction[1] > prediction[0] else 0

    return label

# # Example usage
# url = 'www.bit.ly/jobzila'
# prediction = predict_url(url)
# print('URL:', url)
# print('Prediction:', prediction)

