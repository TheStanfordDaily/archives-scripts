# CloudSearch

## Description 
Use amazon CloudSearch to power archive search. 

## Startup
How to run the contents of this directory
1. Make sure you have [AWS Credentials Setup](#aws-credentials-setup)
1. Create conda environment `conda create -n cloudsearch_env python=3.7.4`
2. Activate conda environment `conda activate cloudsearch_env`
3. Install packages `pip install -r requirements.txt`
4. Run program `incomplete`

## AWS Credentials Setup
Never check in AWS credentials into git. Instead:
1. Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
2. Run `aws configure` in shell, and set your `AWS Access Key ID`, `AWS Secret Access Key` and set `Default region name` to be `us-east-1`.
   1. Note: currently, I don't know what to set as `Default output format`, so I just left it blank.
   2. You can always run `aws configure` again to update these values
   3. Note: your data will be saved to the `~/.aws` directory.

## Files

### `cloudsearch-test.py`
A test file to get myself acquainted with the CloudSearch SDK

### `cloudsearchdomain-test.py`
A test file to get myself acquainted with the CloudSearchDomain SDK

## Todo

## Questions & answers when found & also terms/things which I found confusing
- CloudSearch vs CloudSearch 2?
  - Use CloudSearch2. CloudSearch is the older version (I think pre 2013/4?)
- CloudSearch vs CloudSearchDomain
  - Domain client used to submit search requests and document requests
  - CloudSearch allows you to create and modify domains, define details of that domains like index fields (i.e. searchable fields), scheme define a custom result suggester. This is more of administrative stuff / meta data.
  - CloudSearchDomain is used to upload documents, search for documents, suggest documents. Used for interacting with the actual data.
- [Expression](https://docs.aws.amazon.com/cloudsearch/latest/developerguide/API_Expression.html), [more](https://docs.aws.amazon.com/cloudsearch/latest/developerguide/configuring-expressions.html) - Expressions that can be evaluated dynamically at search time, for sorting search results, or returning coupled information about search results. 
- [Analysis Scheme](https://docs.aws.amazon.com/cloudsearch/latest/developerguide/configuring-analysis-schemes.html) - allows custom text field analysis, to customize search results on text. Probably don't need to use this--default analysis scheme seems legit enough.
- [Paginators](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/paginators.html) - a layer of abstraction for pagination. Pagination is the process of making subsequent requests from an initial request (e.g. initial request returns IDs of search results, then a subsequent request would be to get some data about the documents which the IDs correspond to). I think [this](https://docs.aws.amazon.com/cloudsearch/latest/developerguide/paginating-results.html) is also an example of when to use pagination. 

## Resources
- [5 min introductory video from Amazon](https://www.youtube.com/watch?v=gpG16MFnEH8)
- [45 min introductory video from Amazon](https://www.youtube.com/watch?v=MaKiGbLEDxg) - talks about data types, queries, highlighting, autocomplete etc. 
- [Good starting point](https://docs.aws.amazon.com/cloudsearch/latest/developerguide/what-is-cloudsearch.html) - go down each of the topics in the left sidebar. One notable topic in the sidebar is the API reference. 
- [CloudSearch Developer Resources](https://aws.amazon.com/cloudsearch/developer-resources/) - note the Python doc is out of date. Use boto 3.
- [Python CloudSearch API Ref](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearch.html)
- [Python CloudSearchDomain API Ref](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudsearchdomain.html)