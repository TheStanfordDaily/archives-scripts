# CloudSearch

## Description 
Use amazon CloudSearch to power archive search. 

## Startup
How to run the contents of this directory
1. Run `sh setup.sh` in `cloudsearch/` directory to clone archives text.
2. Make sure you have [AWS Credentials Setup](#aws-credentials-setup)
3. Create conda environment `conda create -n cloudsearch_env python=3.7.4`
4. Activate conda environment `conda activate cloudsearch_env`
5. Install packages `pip install -r requirements.txt`
6. Run program `incomplete`

## AWS Credentials Setup
Never check in AWS credentials into git. Instead:
1. Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
2. Run `aws configure` in shell, and set your `AWS Access Key ID`, `AWS Secret Access Key`, set `Default region name` to be `us-east-1` and set `Default output format` to text 
   1. You can always run `aws configure` again to update these values
   2. Note: your data will be saved to the `~/.aws` directory.

## Files

### `cloudsearch-test.py`
A test file to get myself acquainted with the CloudSearch SDK.
This file shows how to use SDK to 
1. create a domain
2. get domain status
3. configure and show access policies for domain
4. configure and show index fields in domain
5. force domain to index documents
6. define a suggester

Note: you can do many other things, like update scaling parameters with the cloudsearch SDK. Checkout the boto3 docs (linked in [resources](#resources)).

### `cloudsearchdomain-test.py`
A test file to get myself acquainted with the CloudSearchDomain SDK

### `process-archives-text.py`
processes the .txt files in archives-text to cloudsearch readable JSON

### `find-author-titles-archives-text.py`
script to find possible author titles

### `cloudsearch-process-and-upload.py`
an OO program which does same thing as `process-archives-text.py` except neater/better. Designed to be run in parallel (one object/process per year, or year range)

### `docs/search.md`
gives the schema of columns in cloudsearch

## Todo
- experiments testing search/suggest/upload speeds
- create a script to correct document data (many of the documents have repeated text)
- make estimates on size / costs of everything -- figure out optimal scaling option (e.g. search.m1.small)
- change article number to articleLocalID which includes the entire first part of filename, not just the number.
- make setup.sh script which runs `git clone https://github.com/TheStanfordDaily/archives-text.git`
- look into highlighting search hits with Cloudsearch

## Questions & answers when found & also terms/things which I found confusing
- CloudSearch vs CloudSearch 2?
  - Use CloudSearch2. CloudSearch is the older version (I think pre 2013/4?)
- CloudSearch vs CloudSearchDomain
  - Domain client used to submit search requests and document requests. 
  - CloudSearch allows you to create and modify domains, define details of that domains like index fields (i.e. searchable fields), scheme define a custom result suggester. This is more of administrative stuff / meta data. CloudSearch is basically API for the cloudsearch dashboard sidebar, under 'configure domain'
  - CloudSearchDomain is used to upload documents, search for documents, suggest documents. Used for interacting with the actual data.
- [Expression](https://docs.aws.amazon.com/cloudsearch/latest/developerguide/API_Expression.html), [more](https://docs.aws.amazon.com/cloudsearch/latest/developerguide/configuring-expressions.html) - Expressions that can be evaluated dynamically at search time, for sorting search results, or returning coupled information about search results. 
- [Analysis Scheme](https://docs.aws.amazon.com/cloudsearch/latest/developerguide/configuring-analysis-schemes.html) - allows custom text field analysis, to customize search results on text. Probably don't need to use this--default analysis scheme seems legit enough.
- [Paginators](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html) - a layer of abstraction for pagination. Pagination is the process of making subsequent requests from an initial request (e.g. initial request returns IDs of search results, then a subsequent request would be to get some data about the documents which the IDs correspond to). I think [this](https://docs.aws.amazon.com/cloudsearch/latest/developerguide/paginating-results.html) is also an example of when to use pagination. 
- [Domain Statuses & Meanings](https://docs.aws.amazon.com/cloudsearch/latest/developerguide/getting-domain-info.html) - Note: you can still upload documents while domain status is PROCESSING, NEEDS INDEXING or ACTIVE.
- [Index Field](https://docs.aws.amazon.com/cloudsearch/latest/developerguide/configuring-index-fields.html) - index fields contain the data which can be searched/returned. Like the schema of the data.

## Resources
- [5 min introductory video from Amazon](https://www.youtube.com/watch?v=gpG16MFnEH8)
- [45 min introductory video from Amazon](https://www.youtube.com/watch?v=MaKiGbLEDxg) - talks about data types, queries, highlighting, autocomplete etc. 
- [Good starting point](https://docs.aws.amazon.com/cloudsearch/latest/developerguide/what-is-cloudsearch.html) - go down each of the topics in the left sidebar. One notable topic in the sidebar is the API reference. 
- [CloudSearch Developer Resources](https://aws.amazon.com/cloudsearch/developer-resources/) - note the Python doc is out of date. Use boto 3.
- [Python CloudSearch SDK/API Ref](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html)
- [Python CloudSearchDomain SDK/API Ref](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearchdomain.html)
- [Some more doc](https://github.com/awsdocs/amazon-cloudsearch-developer-guide/tree/master/doc_source)
- [Outdated guide, but still useful conceptually](https://boto.readthedocs.io/en/latest/cloudsearch_tut.html)