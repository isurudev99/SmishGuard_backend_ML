from collections import Counter
from random import randint

from fastapi import FastAPI
from pydantic import BaseModel

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import ssl

from Database.database import databaseSearch
from HTML_Features_Analysis.HTML_main import HTML_feature_classification
from SMS_classification.load_model_for_predictions import predictions
from URL_Classification.XGBoost import XGBoost_Predictions
from URL_Classification.distilbert import predict_url

app = FastAPI()


class RequestPayload(BaseModel):
    text: str


@app.get("/cybersmish")
def predict_output():
    prediction = randint(0, 1)
    return {"predictions": prediction}


@app.post("/cybersmish/post")
async def receive_message(payload: RequestPayload):
    # call database
    message = payload.text

    print(message)

    pred_list = []
    zero_list = []
    one_list = []

    if message is not None:
        sms_classification, url = predictions(message)
        pred_list.append(sms_classification)
        # print('\n\n\nURL is:', url)

        if url is not None:
            # check URL on database 
            for url_item in url:
                actual_url = get_actual_URL(url_item)
                if actual_url == ['ERROR']:
                    pred_list.append(1)
                else:
                    databaseReturn = databaseSearch(actual_url)
                    if databaseReturn is not None:
                        pred_list.append(databaseReturn)
                    else:
                        pred_list.remove(sms_classification)
                        XGBoost_prediction, distillBERT_prediction, RF_predicted_label, BERT_predicted_label = call_URL_models(actual_url)
                        pred_list.append(XGBoost_prediction)
                        pred_list.append(distillBERT_prediction)
                        pred_list.append(RF_predicted_label)
                        pred_list.append(BERT_predicted_label)

                    for pred in pred_list:
                        if pred == 0:
                            zero_list.append(pred)
                        else:
                            one_list.append(pred)


    print(pred_list)
    # print("length of pred_list:",len(pred_list))

    if len(pred_list) == 1:
        most_common_prediction = pred_list[0]
    elif len(pred_list) == 2 and pred_list[0] == 0 and pred_list[1] == 0:
        most_common_prediction = 0
    elif len(pred_list) == 2 and pred_list[0] == 1 and pred_list[1] == 1:
        most_common_prediction = 1
    elif len(pred_list) == 2 and pred_list[0] == 0 and pred_list[1] == 1:
        most_common_prediction = 1
    elif len(pred_list) == 2 and pred_list[0] == 1 and pred_list[1] == 0:
        most_common_prediction = 0
    elif len(pred_list) == 4 and len(zero_list) > len(one_list) == 0:
        most_common_prediction = 0
    elif len(pred_list) == 4 and len(one_list) > len(zero_list) == 0:
        most_common_prediction = 1
    elif len(pred_list) == 4 and len(zero_list) == len(one_list):
        most_common_prediction = sms_classification
    
    # most_common_prediction = Counter(pred_list).most_common(1)[0][0]

    # count predictions
    # if RF_predicted_label and BERT_predicted_label is not None:
    #     if RF_predicted_label == BERT_predicted_label:
    #         print("HTML classification says URL is Phishing or legitimate")

    print(most_common_prediction)
    return {"predictions": most_common_prediction}


def call_URL_models(url):
    # check url from database 
    
    distillBERT_prediction = predict_url(url)
    RF_predicted_label, BERT_predicted_label = HTML_feature_classification(url)
    XGBoost_prediction = XGBoost_Predictions(url)

    return XGBoost_prediction, distillBERT_prediction, RF_predicted_label, BERT_predicted_label


def get_actual_URL(input_url):
    url = str(input_url) 
    try:
        # Create an SSL context with certificate verification disabled
        # ssl_context = ssl.create_default_context()
        # ssl_context.check_hostname = False
        # ssl_context.verify_mode = ssl.CERT_NONE

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode, without opening a browser window
        # chrome_options.add_argument("--lang=en-US")  # Set the browser language to English (United States)
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration to prevent errors
        chrome_options.add_argument("--no-sandbox")  # Disable sandbox mode to prevent issues in some environments
        chrome_options.add_argument('--disable-setuid-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=1920,1080")
        
        with webdriver.Chrome(options=chrome_options) as driver:
            driver.get(url)
            get_url = driver.current_url

            print("Actual_URL is :",get_url)

        return get_url
    
    except Exception as e:
        print(f"Error processing file {url}: {e}")
        return ['ERROR']
