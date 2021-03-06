'''
Designed to be run in parallel, uploads processed archives-text
data in 5 mb batches

designed to be run in the cloudsearch/ directory

you should check logs for jumps in years once done. If there are any, then it's likely the last year prior to the jump
didn't successfully upload, and you'll have to reupload those years.
'''

import boto3
import os
import re
import json
from multiprocessing import Pool
import time


DOC_ENDPOINT = 'https://doc-archives-text-cloudsearch-rba7owuzh6kn24pic2yudkawpe.us-east-1.cloudsearch.amazonaws.com'
DOC_CLIENT = boto3.client('cloudsearchdomain', endpoint_url=DOC_ENDPOINT)

MAX_BATCH_SIZE = 5242880 # 5 MB
MAX_FILE_SIZE = 1048576 # 1 MB

ARCHIVES_TEXT_PATH = './archives-text/'
LOG_PATH = './logs/'

VALID_ARTICLE_TYPES = ['article', 'advertisement',]
VALID_AUTHOR_TITLES = ['', 'SENIOR STAFF WRITER', 'STAFF WRITER', 'DESK EDITOR', 'CONTRIBUTING WRITER', 
'MANAGING EDITOR', 'EDITOR IN CHIEF', 'DEPUTY EDITOR', 'EXECUTIVE EDITOR', 'STAFF', 
'ASSU President', 'ASSU Parlimentarian', 'STAFF FOOTBALL WRITERS', 'FASHION COLUMNIST', 
'FOOTBALL EDITOR', 'ARTS EDITOR', 'FOOD EDITOR', 'FOOD DINING EDITOR', 'OPINIONS DESK',
'FOOD DRUNK EDITOR', 'FELLOW', 'DAILY INTERN', 'CONTRIBUTING EDITOR', 'MANAGING WRITER',
'GUEST COLUMNIST', 'SEX GODDESS', 'GUEST COLUMNISTS', 'EDITORIAL STAKE', 'CONTRIBUTING YANKEE',
'SPECIAL CONTRIBUTOR', 'EDITORIAL BOARD', 'CONTRIBUTING WRITER', 'EDITORIAL STAFF', 'FILM CRITIC',
'HEALTH EDITOR', 'ASSHOLE', 'INTERMISSION', 'NEWS EDITOR', 'CLASS PRESIDENT', 'ASSOCIATED PRESS',
'AP SPORTS WRITER', 'AP BASEBALL WRITER', 'WEEKLY COLUMNIST', 'HEALTH COLUMNIST', 'ASSOCIATED EDITOR',
'ASSOCIATE EDITOR', 'SPORTS EDITOR', 'EDITOR THE DAILY', ]

# for multiprocessing; set this to a reasonable number.
POOL_SIZE = 1 # note: large pools (>4 or 5) don't seem to mesh well w/ cloudsearch

class Logger:
    def __init__(self, path, basename):
        self.fullpath = path + basename + '.log'
        f = open(self.fullpath, 'w')
        f.write("logger start\n")
        f.close()

    def log(self, message):
        f = open(self.fullpath, 'a') # open and close here for live updates
        f.write(message + "\n")
        f.close()

    def get_fullpath(self):
        return self.fullpath

    def __del__(self):
        f = open(self.fullpath, 'a') # open and close here for live updates
        f.write("logger done\n")
        f.close()
        
class ArchivesTextProcessor:
    def __init__(self, base_path, startYear, endYear, batchSizeInBytes, docClient):
        self.base_path = base_path
        self.startYear = startYear
        self.endYear = endYear
        self.batchSizeInBytes = batchSizeInBytes
        self.docClient = docClient
        self.currentSizeInBytes = 0
        self.logger = Logger(LOG_PATH, str(startYear))
        self.is_done = False
        print('logs outputted to %s' % self.logger.get_fullpath())

        # initialize some data
        self.years_left = list(range(startYear, endYear))
        self.currentYear = None
        self.move_to_next_year()
        self.months_left_in_year = None
        self.set_months_left_in_year()
        self.currentMonth = None
        self.move_to_next_month()
        self.days_left_in_month = None
        self.set_days_left_in_month()
        self.currentDay = None
        self.move_to_next_day()
        self.articles_left_in_day = None
        self.set_articles_left_in_day()
        self.currentArticle = None
        self.move_to_next_article()

    def __del__(self):
        del self.logger
    '''
    the following are functions to help us iterate through the files in archives-text
    '''
    def are_we_done(self):
        return self.is_done

    def get_current_path(self, level):
        if(level == 'year'):
            return self.base_path + str(self.currentYear).zfill(4) + '/'
        elif(level == 'month'):
            return self.base_path + str(self.currentYear).zfill(4) + '/' + str(self.currentMonth).zfill(2) + '/'
        elif(level == 'day'):
            return self.base_path + str(self.currentYear).zfill(4) + '/' + str(self.currentMonth).zfill(2) + '/' + str(self.currentDay).zfill(2) + '/'
        elif(level == 'article'):
            return self.base_path + str(self.currentYear).zfill(4) + '/' + str(self.currentMonth).zfill(2) + '/' + str(self.currentDay).zfill(2) + '/' + self.currentArticle
        else:
            self.logger.log('ERROR: is an invalid level' % level)

    def set_months_left_in_year(self):
        months = os.listdir(self.get_current_path('year'))
        filtered_months = []
        for i in range(0, len(months)):
            try:
                filtered_months.append(int(months[i]))
            except:
                continue
        filtered_months.sort()
        self.months_left_in_year = filtered_months

    def set_days_left_in_month(self):
        days = os.listdir(self.get_current_path('month'))
        filtered_days = []
        for i in range(0, len(days)):
            try:
                filtered_days.append(int(days[i]))
            except:
                continue
        filtered_days.sort()
        self.days_left_in_month = filtered_days

    def set_articles_left_in_day(self):
        articles = os.listdir(self.get_current_path('day'))
        filtered_articles = []
        for i in range(0, len(articles)):
            try:
                filtered_articles.append(articles[i])
            except:
                continue
        filtered_articles.sort()
        self.articles_left_in_day = filtered_articles
        
    # returns -1 if we can't move anymore (i.e. we're done), 1 on success
    def move_to_next_year(self):
        if(len(self.years_left) == 0):
            self.logger.log('done')
            self.is_done = True
            return -1
        else:
            self.currentYear = self.years_left.pop()
            return 1

    # returns -1 if we can't move anymore (i.e. we're done), 1 on success
    def move_to_next_month(self):
        while(len(self.months_left_in_year) == 0):
            if(self.move_to_next_year() < 0):
                return -1
            self.set_months_left_in_year()
        self.currentMonth = self.months_left_in_year.pop()
        return 1
        
    # returns -1 if we can't move anymore (i.e. we're done), 1 on success
    def move_to_next_day(self):
        while(len(self.days_left_in_month) == 0):
            if(self.move_to_next_month() < 0):
                return -1
            self.set_days_left_in_month()
        self.currentDay = self.days_left_in_month.pop()
        return 1

    def move_to_next_article(self):
        while(len(self.articles_left_in_day) == 0):
            if(self.move_to_next_day() < 0):
                return -1
            self.set_articles_left_in_day()
        self.currentArticle = self.articles_left_in_day.pop()
        return 1
    
    '''
    the following are functions to process data in the .txt files in archives-text
    '''
    def get_current_publish_date(self):
        return '%s-%s-%sT12:00:00Z' %(str(self.currentYear).zfill(4), str(self.currentMonth).zfill(2), str(self.currentDay).zfill(2)) # default set time to 12:00, since we don't care about that.

    # detects if text has repeated substrings and removes if true
    # this seems like a leetcode problem lol. I'm using this as a ref https://www.geeksforgeeks.org/python-check-if-string-repeats-itself/
    def removeRepeats(self, text):
        if(len(text) < 2):
            return text
        
        res = None
        temp = (text + text).find(text, 1, -1)
        if(temp != -1):
            res = text[:temp]
            # self.logger.log(self.get_current_path('article'))
            # self.logger.log(res)
            return res
        return text

    def get_current_article_data(self):
        with open(self.get_current_path('article'), 'r') as f:
            articleRawText = f.read()
            articleLines = articleRawText.splitlines()

            # perform some sanity checks 
            try:
                if(not articleLines[0].startswith('#')):
                    self.logger.log('error in first line of article %s' % self.get_current_path("article"))
                if(not articleLines[1].startswith('##')):
                    self.logger.log('error in second line of article %s' % self.get_current_path("article"))
                if(not articleLines[2].startswith('###')):
                    self.logger.log('error in third line of article %s' % self.get_current_path("article"))
            except:
                pass

            # extract data
            try:
                title = re.sub('\s+', ' ', articleLines[0][2:].strip()) # get rid of extra whitespace, plus skip extra chars
                subtitle = re.sub('\s+', ' ', articleLines[1][3:].strip()) 
                author_raw = re.sub('\s+', ' ', articleLines[2][4:].strip())
            except:
                title = ""
                subtitle = ""
                author_raw = ""
                
            author = author_raw
            authorTitle = ''
            for possibleTitle in VALID_AUTHOR_TITLES:
                title_index = author_raw.upper().find(possibleTitle)
                if(title_index > 0):
                    authorTitle = possibleTitle
                    author = author[0:title_index]
                    break

            articleText = ''
            for i in range(3, len(articleLines)):
                articleLines[i] += '\n'
            articleTextJoined = articleText.join(articleLines[3:])
            articleText = self.removeRepeats(articleTextJoined)
            filename_parts = self.currentArticle.split('.')
            articleType = filename_parts[1]
            articleNumber = filename_parts[0]

            return {
                'article_text': articleText,
                'article_type': articleType,
                'article_number': articleNumber,
                'title': title,
                'subtitle': subtitle,
                'author': author,
                'author_title': authorTitle,
                'publish_date': self.get_current_publish_date()
            }

    def pretty_print_current_article_data(self):
        current_article_data = self.get_current_article_data()
        print('----------------------------------------------------------')
        print('title:', current_article_data['title'])
        print('subtitle:', current_article_data['subtitle'])
        print('author:', current_article_data['author'])
        print('author_title:', current_article_data['author_title'])
        print('article_type:', current_article_data['article_type'])
        print('article_number:', current_article_data['article_number'])
        print('publish_date:', current_article_data['publish_date'])
        print('text sample:', current_article_data['article_text'])
        print('----------------------------------------------------------')

    """
    the following are functions to upload data to cloudsearch
    """
    def create_current_article_cloudsearch_add_request_JSON(self):
        fields = self.get_current_article_data()
        return {
            'type': 'add',
            'id': fields['publish_date'] + fields['article_type'] + str(fields['article_number']),
            'fields': fields
        }

    def get_current_add_request_size_in_bytes(self):
        current_request = self.create_current_article_cloudsearch_add_request_JSON()
        size = len(json.dumps(current_request))
        if(size > MAX_FILE_SIZE):
            self.logger.log('%s is too big!' % self.get_current_path("article"))
        return size

    def create_batch_article_cloudsearch_add_request_JSON(self):
        self.logger.log('creating a new batch, starting at article %s' % self.get_current_path("article"))
        current_batch = []
        article_count = 0
        # this is pretty inefficient b/c we're computing the add request 3 times.
        while(self.currentSizeInBytes + self.get_current_add_request_size_in_bytes() < self.batchSizeInBytes):
            article_count += 1
            current_batch.append(self.create_current_article_cloudsearch_add_request_JSON())
            self.currentSizeInBytes += self.get_current_add_request_size_in_bytes()
            not_done = self.move_to_next_article()
            if(not_done < 0):
                break # we've reached the last article
        self.logger.log('created batch, ended at article %s, has size bytes %d and total of %d articles' % (self.get_current_path("article"), self.currentSizeInBytes, article_count))
        self.currentSizeInBytes = 0
        return current_batch

    def upload_article_batch_to_cloudsearch(self):
        self.logger.log("making a batch upload")
        batch = json.dumps(self.create_batch_article_cloudsearch_add_request_JSON())
        self.logger.log("sending data to cloudsearch")
        response = self.docClient.upload_documents(documents=batch, contentType="application/json")
        self.logger.log("cloudsearch response:")
        self.logger.log(str(response))
        if(response['status'] != 'success'):
            self.logger.log("THERE WAS AN ERROR IN UPLOADDING THIS BATCH. WE DON'T CURRENTLY HAVE ERROR HANDLING, YOU WILL NEED TO RETRY THIS BATCH MANUALLY")
        self.logger.log("done with batch upload")

"""
some tests
"""
def test_upload_single_batch_from_year(year):
    print("starting to test process year %d" % year)
    testProcessor = ArchivesTextProcessor(ARCHIVES_TEXT_PATH, year, year + 1, MAX_BATCH_SIZE, DOC_CLIENT)
    testProcessor.upload_article_batch_to_cloudsearch()
    time.sleep(1)
    print("done with test processing year %d" % year)

def multiprocessing_test():
    with Pool(POOL_SIZE) as p:
        p.map(test_upload_single_batch_from_year, list(range(1900, 1902)))

def tests():
    print('tests:')
    testProcessor = ArchivesTextProcessor(ARCHIVES_TEXT_PATH, 1901, 1902, MAX_BATCH_SIZE, DOC_CLIENT)
    print(testProcessor.create_current_article_cloudsearch_add_request_JSON())
    # # uncomment if you want to see some article data be printed out
    # for i in range(10):
    #     print(testProcessor.get_current_path('article'))
    #     print("size:", testProcessor.get_current_add_request_size_in_bytes())
    #     testProcessor.pretty_print_current_article_data()
    #     testProcessor.move_to_next_article()
    # print('if you compare with https://github.com/TheStanfordDaily/archives-text/tree/master/1899/12 you should see matching results')
    
    # uncomment to test a processing of range between 1899 - 1901
    # while(not testProcessor.are_we_done()):
    #     testProcessor.create_batch_article_cloudsearch_add_request_JSON()

    # uncomment to test a single batch upload (note: will take a while if aws is slow)
    # testProcessor.upload_article_batch_to_cloudsearch()

    # uncomment to test multiprocessed single batch upload
    # multiprocessing_test()

"""
for actually uploading archive text
"""
def process_and_upload_year(year):
    yearProcessor = ArchivesTextProcessor(ARCHIVES_TEXT_PATH, year, year + 1, MAX_BATCH_SIZE, DOC_CLIENT)
    print("starting to process year %d" % year)
    while(not yearProcessor.are_we_done()):
        yearProcessor.upload_article_batch_to_cloudsearch()
    print("done with processing year %d" % year)

def uploadYears(startYear, endYear):
    with Pool(POOL_SIZE) as p:
        p.map(process_and_upload_year, list(range(startYear, endYear + 1)))

# multiprocessed full upload of archives text
def upload_archives_text():
    uploadYears(1892, 2014)

def upload_archives_text_test():
    uploadYears(1969, 1969)

def main():
    # tests()
    # upload_archives_text()
    upload_archives_text_test()

if __name__ == '__main__':
    main()