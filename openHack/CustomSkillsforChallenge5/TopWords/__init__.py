import logging
import azure.functions as func
import json
from string import punctuation
from collections import Counter

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        body = json.dumps(req.get_json())
    except ValueError:
        return func.HttpResponse("Invalid body", status_code=400)
    
    if body:
        result = compose_response(body)
        return func.HttpResponse(result, mimetype="application/json")
    else:
        return func.HttpResponse("Invalid body", status_code=400)


def compose_response(json_data):
    values = json.loads(json_data)['values']
    
    # Prepare the Output before the loop
    results = {}
    results["values"] = []
    
    for value in values:
        output_record = transform_value(value)
        if output_record != None:
            results["values"].append(output_record)
    return json.dumps(results, ensure_ascii=False)

## Perform an operation on a record
def transform_value(value):
    try:
        recordId = value['recordId']
    except AssertionError as error:
        return None

    # Validate the inputs
    try:         
        assert ('data' in value), "'data' field is required."
        data = value['data']
        assert ('text' in data), "'text' field is required in 'data' object."
    except AssertionError  as error:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Error:" + error.args[0] }   ]       
            })

    try:                
        # run code
        output = get_top_ten_words(value['data']['text'])
        # Here you could do something more interesting with the inputs

    except:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Could not complete operation for record." }   ]       
            })

    return ({
            "recordId": recordId,
            "data": output
                    
            })

def get_top_ten_words(text):

    # Array of stop words to be ignored
    stopwords = ['', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
    "youre", "youve", "youll", "youd", 'your', 'yours', 'yourself', 
    'yourselves', 'he', 'him', 'his', 'himself', 'she', "shes", 'her', 
    'hers', 'herself', 'it', "its", 'itself', 'they', 'them', 
    'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 
    'this', 'that', "thatll", 'these', 'those', 'am', 'is', 'are', 'was',
    'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 
    'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 
    'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 
    'about', 'against', 'between', 'into', 'through', 'during', 'before', 
    'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 
    'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 
    'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can', 'will',
    'just', "dont", 'should', "shouldve", 'now', "arent", "couldnt", 
    "didnt", "doesnt", "hadnt", "hasnt", "havent", "isnt", "mightnt", "mustnt",
    "neednt", "shant", "shouldnt", "wasnt", "werent", "wont", "wouldnt", "shall"]

    # Empty JSON structure in which to return the results
    result_json = {"words":[]}

    try:
        # remove numeric digits
        text = ''.join(c for c in text if not c.isdigit())

        # remove punctuation and make lower case
        text = ''.join(c for c in text if c not in punctuation).lower()

        # remove stopwords
        text = ' '.join(w for w in text.split() if w not in stopwords)

        # Count the words and get the most common 10
        wordcount = Counter(text.split()).most_common(10)
        words = [w[0] for w in wordcount]

        # Add the top 10 words to the output for this text record
        result_json["words"] = words

        # return the results
        return result_json

    except Exception as ex:
        print(ex)