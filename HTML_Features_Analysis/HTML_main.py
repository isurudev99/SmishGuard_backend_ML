import pandas as pd
import pickle
import warnings
import requests

warnings.filterwarnings("ignore", category=RuntimeWarning)
# import ssl
from HTML_Features_Analysis.extract_numarical_values_functions import extract_numarical_values, extract_text_features, extract_links
from HTML_Features_Analysis.P_Tag_pred import predict_sentiment


# convert short URL's to its real form
# def expand_short_url(short_url):
#     if short_url.startswith("http://bit.ly/") or short_url.startswith("https://t.co/"):
#         try:
#             response = requests.head(short_url, allow_redirects=True, verify=False)
#             long_url = response.url
#             return long_url
#         except requests.exceptions.RequestException as e:
#             print(f"Error expanding short URL: {e}")
#     else:
#         print("Given URL is not a shortened URL.")
#         return short_url


# compre the final predictions and print the output 
# def mergre_pred(RF_predicted_label, BERT_predicted_label):
#     if BERT_predicted_label != None:
#         if RF_predicted_label != None:
#             if BERT_predicted_label == RF_predicted_label:
#                 return BERT_predicted_label
#             else:
#                 # ========== add fucntions to call for VirusTotal API =============
#                 return RF_predicted_label


def HTML_feature_classification(url):

    # url = expand_short_url(url)
    print(url)

    # get numarical values from extract_numarical_values in internal_external.py file 
    script_ratio, css_ratio, img_ratio, a_tag_ratio, a_tag_null_ratio, null_ratio, form_count, total_links = extract_numarical_values(
        url)
    print(script_ratio, css_ratio, img_ratio, a_tag_ratio, a_tag_null_ratio, null_ratio, form_count, total_links)

    results = extract_links(total_links, url)
    if results is not None:
        Internal_Links_Ratio, External_Links_Ratio, External_to_Internal_Ratio, error_hyperlinks_ratio = results
        print(results)

    # load trained random forest model
    MODELSPATH = 'HTML_Features_Analysis/models/RF_model.pkl'
    # Load the saved model
    with open(MODELSPATH, 'rb') as f:
        rf = pickle.load(f)

    # Define a new sample to predict
    new_sample = {
        'script_ratio': script_ratio,
        'css_ratio': css_ratio,
        'img_ratio': img_ratio,
        'a_ratio': a_tag_ratio,
        'a_null_ratio': a_tag_null_ratio,
        'null_ratio': null_ratio,
        'internal_links_ratio': Internal_Links_Ratio,
        'external_links_ratio': External_Links_Ratio,
        'external_to_internal_ratio': External_to_Internal_Ratio,
        'form_count': form_count,
        'error_link_count': error_hyperlinks_ratio
    }

    # Convert the new sample to a DataFrame and predict its label
    new_sample_df = pd.DataFrame([new_sample])

    RF_predicted_label_list = rf.predict(new_sample_df)
    RF_predicted_label = RF_predicted_label_list[0]

    # ============================ Text features Prediction ===========================================

    text_value = extract_text_features(url)

    # if isinstance(text_value, list):
    #     # If 'text' is a list, join its elements into a single string
    #     text_value = ' '.join(text_value)

    # text = 'this is legitimate content. please sign with gmail username and password in here'
    if text_value is not None:

        if isinstance(text_value, list):
        # If 'text_value' is a list, join its elements into a single string
            text_value = ' '.join(text_value)

        BERT_predicted_label = predict_sentiment(text_value)
        print("\n\nBERT Predicted Label:", BERT_predicted_label)
    else:
        print("the Text_value varible is None")
        BERT_predicted_label = 0

    # print("RF Predicted label:", RF_predicted_label)

    # # ===================== Print Predictions Output =======================
    # if mergre_pred(RF_predicted_label, BERT_predicted_label) == 1:
    #     prediction = 'Phishing website'
    # else:
    #     prediction = 'Legitimate website'

    return RF_predicted_label, BERT_predicted_label

# url = 'https://baiscopedownloads.co/'
# print(HTML_feature_classification(url))