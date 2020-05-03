"""
Explorations for CloudSearchDomain

goes hand in hand w/ cloudsearch-test.py--assumes that it's already been run / the 
domain has already been created and configured. 

For ref, our domain two fields:
1. testfieldtext - type: text / default value: 'default value' / return enabled: true /
sort enabled: true / highlight enabled: true / analysis scheme: '_en_default'
2. testfieldint - type: int / default value: 0 / facet enabled: true / return enabled: true /
sort enabled: true / search enabled: true 

We also have a suggester for the textfieldtext field:
testsuggester - source field: testfieldtext / fuzzymatching: low / sortexpression: testfieldint

another example - https://gist.github.com/reedobrien/a7cf32c3e4e6cad0deb6

todo: example for suggest
"""
import boto3
import json
import uuid
import random

word_list = []
with open('random-words.txt') as f:  # or whatever the wordlist is saved as
  for line in f.readlines():
    index, word = line.strip().split('\t')
    word_list.append(word)

SEARCH_ENDPOINT = "SEARCH-ENDPOINT-HERE"
DOC_ENDPOINT = "DOC-ENDPOINT-HERE"

search_client = boto3.client('cloudsearchdomain', endpoint_url=SEARCH_ENDPOINT)
doc_client = boto3.client('cloudsearchdomain', endpoint_url=DOC_ENDPOINT)

"""
some sample data for us to work with

Note: must specify type/unique id/name-value pair for each document field
Note: play around with this data, see how to get get cloudsearch to throw 
errors and then how to fix those errors.
"""
SAMPLE_DOCS = [
    {
        "type": "add",
        "id": "1",
        "fields": {
            "testfieldtext": "test 1",
            "testfieldint": 1
        }
    },
    {
        "type": "add",
        "id": "2",
        "fields": {
            "testfieldtext": "test 2",
            "testfieldint": 2
        }
    },
    {
        "type": "add",
        "id": "3",
        "fields": {
            "testfieldtext": "test 3",
            "testfieldint": 3
        }
    }
]

"""
docs:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearchdomain.html#CloudSearchDomain.Client.search
https://docs.aws.amazon.com/cloudsearch/latest/developerguide/searching.html

todo: explore filterQuery (https://docs.aws.amazon.com/cloudsearch/latest/developerguide/filtering-results.html)
"""
def makeSearch():
    """
    query - required parameter, uses simple queryParser by default. simple query parser searches all text 
    and text-array fields by default.
    See here for query syntax https://docs.aws.amazon.com/cloudsearch/latest/developerguide/search-api.html

    size limits our search to the top 5 hits. 
    """
    testSearch1 = "+test"
    print("\nMaking search", testSearch1)
    response = search_client.search(query=testSearch1, size=5)
    print(response, "\n")

"""
docs
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearchdomain.html#CloudSearchDomain.Client.upload_documents
https://docs.aws.amazon.com/cloudsearch/latest/developerguide/uploading-data.html
https://docs.aws.amazon.com/cloudsearch/latest/developerguide/preparing-data.html

Q: what if we don't include a field in data? 
A: things should break (need name-value pair for each doc field)
Q: what if we have too many fields in data?

Q: what if we submit same data multiple times?

Q: what if ID not unique? 
    And all other data identical / and all other data different

Note: if you go to console after upload, you should now be able
to see your docs and also search them!

Furthermore you should be able to get results from makeSearch()!
"""
def makeDocUpload(documentsJSON):
    print("\nMaking Doc Upload")
    response = doc_client.upload_documents(documents=documentsJSON, contentType="application/json")
    print(response,"\n")

"""
documents is a list of python dicts
"""
def formatDocsJSON(documents):
    return json.dumps(documents)

"""
just for testing
"""
def generateRandomSampleDocs(numDocs):
    randomDocs = []
    for i in range(numDocs):
        randomDocs.append({
            "type": "add",
            "id": str(uuid.uuid4().int),
            "fields": {
                "testfieldtext": " ".join([word_list[random.randrange(0, len(word_list))] for i in range(4)]),
                "testfieldint": random.randint(0, 100)
            }
        })
    return randomDocs

def main():
    makeSearch()
    makeDocUpload(formatDocsJSON(SAMPLE_DOCS))
    makeDocUpload(formatDocsJSON(generateRandomSampleDocs(1000)))

if __name__ == '__main__':
    main()