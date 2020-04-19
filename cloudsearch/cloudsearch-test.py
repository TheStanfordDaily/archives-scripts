"""
Exploration for CloudSearch

Currently, this program gives examples for how to:
1. create a domain
2. get domain status
3. configure and show access policies for domain
4. configure and show index fields in domain
5. force domain to index documents
"""

import boto3

client = boto3.client('cloudsearch')

# some constants used in this demo
MY_IP = "75.188.62.170" # maybe I shouldn't check in my IP. 
DN = "dev-alex"
# this is just a test access policy. You can make your own. Documented here: https://docs.aws.amazon.com/cloudsearch/latest/developerguide/configuring-access.html
AP = "{\"Version\":\"2012-10-17\",\"Statement\":[{\
  \"Sid\":\"search_only\",\
  \"Effect\":\"Allow\",\
  \"Principal\": \"*\",\
  \"Action\":\"cloudsearch:search\",\
  \"Condition\":{\"IpAddress\":{\"aws:SourceIp\":\""+MY_IP+"\"}}}\
]}"
# docs for index fields here https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.define_index_field
IF_TEXT = {
    'IndexFieldName': 'testfieldtext',
    'IndexFieldType': 'text',
    'TextOptions': {
        'DefaultValue': 'default value',
        'ReturnEnabled': True,
        'SortEnabled': True,
        'HighlightEnabled': True,
        'AnalysisScheme': '_en_default_'
    }
}
IF_INT = {
    'IndexFieldName': 'testfieldint',
    'IndexFieldType': 'int',
    'IntOptions': {
        'DefaultValue': 0,
        'FacetEnabled': True,
        'SearchEnabled': True,
        'ReturnEnabled': True,
        'SortEnabled': True
    }
}

"""
https://docs.aws.amazon.com/cloudsearch/latest/developerguide/creating-domains.html

Q: what if I create a domain w/ the same domainName multiple times?
A: Nothing bad, it seems. You don't create a new domain, and it doesn't seem like you erase the existing one (need confirmation on this)
Q: what if I try to interact with this domain while it's still loading?
A: note sure exactly, but showAccessPolicies does give an output...
Q: what size of domain is created?
A: From dashboard: "Your domain is deployed on a total of 1 search.m1.small instance. 
    The search index for this domain is split across 1 partition." This is the
    smallest size
    
-----------------------------------------------------
Expected effect:
If you go to CloudSearch Dashboard, you should see your new domain! Status will be LOADING
"""
def createDomain(domainName):
    print("\nCreating Domain", domainName)
    response = client.create_domain(DomainName=domainName)
    print(response,"\n")

"""
tells us state/status of domain
"""
def getDomainStatus(domainName):
    print("\nDomain status", domainName)
    response = client.describe_availability_options(DomainName=domainName)
    print(response['AvailabilityOptions']['Status']['State'], "\n")

"""
displays current access policies for domain w/ name domainName
doc: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.update_service_access_policies
"""
def showAccessPolicies(domainName):
    print("\nCurrent Access Policies for", domainName)
    response = client.describe_service_access_policies(DomainName=domainName)
    print(response["AccessPolicies"]["Options"], "\n")

"""
AccessPolicies(string) - The access rules you want to configure. These rules replace any existing rules.
https://docs.aws.amazon.com/cloudsearch/latest/developerguide/configuring-access.html for description of this string

Q: how to add multiple policies? Can I concat the result of showAccessPolicies to the new policy that I want to add?
A: idk yet

Interesting: this query sends the domain into PROCESSING status.

Super annoying: reading through the doc on how tf to format policies / what each of the parts of a policy means.  
"""
def configureAccessPolicies(domainName, policies):
    print("\nAdding Access Policies for", domainName)
    response = client.update_service_access_policies(DomainName=domainName, AccessPolicies=policies)
    print(response,"\n")

"""
lists the existing index fields
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.describe_index_fields
Note: can also add FieldNames parameter to get only specific fields
"""
def showIndexFields(domainName):
    print("\nCurrent Index Fields for", domainName)
    response = client.describe_index_fields(DomainName=domainName) 
    fields = response['IndexFields']
    for field in fields:
        print("Found field with name", field['Options']['IndexFieldName'], "and type", field['Options']['IndexFieldType'])
    print("\n")

"""
indexField is a dict, described here 
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html#CloudSearch.Client.define_index_field
and here
https://docs.aws.amazon.com/cloudsearch/latest/developerguide/configuring-index-fields.html

Note: indexDield.IndexFieldName must be unique. Must also match this pattern: [a-z][a-z0-9_]*\*?|\*[a-z0-9_]* (note: lower case alphanumeric + regex matching) 
SourceField - "Specifying a source copies data from one field to another, enabling you to use the same source data in different ways by configuring different 
options for the fields. You can use a wildcard (*) when specifying the source name to copy data from all fields that match the specified pattern."

Q: if have same indexField.IndexFieldName, does it overwrite / modify?
A: yes.
Q: indexField is appended?
A: yes.
"""
def configureIndexFields(domainName, indexField):
    print("\nConfiguring Index Fields for", domainName)
    response = client.define_index_field(DomainName=domainName, IndexField=indexField)
    print(response,"\n")

"""
need to be done every time we configure index fields, in order to use options w/ OptionStatus RequiresIndexDocuments
"Tells the search domain to start indexing its documents using the latest indexing options. "

Sends domain status into PROCESSING
"""
def indexDocuments(domainName):
    print("\nIndexing documents for", domainName)
    response = client.index_documents(DomainName=domainName)
    print(response,"\n")

def main():
    createDomain(DN)
    getDomainStatus(DN)
    configureAccessPolicies(DN, AP) # commented out, b/c it throws the domain into PROCESSING. 
    showAccessPolicies(DN)
    showIndexFields(DN)
    configureIndexFields(DN, IF_TEXT)
    configureIndexFields(DN, IF_INT)
    indexDocuments(DN)

if __name__ == '__main__':
    main()