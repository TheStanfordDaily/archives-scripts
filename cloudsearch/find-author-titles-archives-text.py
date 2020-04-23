"""
to find possible author titles
"""

import os
import re

ARCHIVES_TEXT_PATH = "PATH_HERE"

# note: if see one, safe to assume goes to end?
KNOWN_TITLES = ['SENIOR STAFF WRITER', 'STAFF WRITER', 'DESK EDITOR', 'CONTRIBUTING WRITER', 
'MANAGING EDITOR', 'EDITOR IN CHIEF', 'DEPUTY EDITOR', 'EXECUTIVE EDITOR', 'STAFF', 
'ASSU President', 'ASSU Parlimentarian', 'STAFF FOOTBALL WRITERS', 'FASHION COLUMNIST', 
'FOOTBALL EDITOR', 'ARTS EDITOR', 'FOOD EDITOR', 'FOOD DINING EDITOR', 'OPINIONS DESK',
'FOOD DRUNK EDITOR', 'FELLOW', 'DAILY INTERN', 'CONTRIBUTING EDITOR', 'MANAGING WRITER',
'GUEST COLUMNIST', 'SEX GODDESS', 'GUEST COLUMNISTS', 'EDITORIAL STAKE', 'CONTRIBUTING YANKEE',
'SPECIAL CONTRIBUTOR', 'EDITORIAL BOARD', 'CONTRIBUTING WRITER', 'EDITORIAL STAFF', 'FILM CRITIC',
'HEALTH EDITOR', 'ASSHOLE', 'INTERMISSION', 'NEWS EDITOR', 'CLASS PRESIDENT', 'ASSOCIATED PRESS',
'AP SPORTS WRITER', 'AP BASEBALL WRITER', 'WEEKLY COLUMNIST', 'HEALTH COLUMNIST', 'ASSOCIATED EDITOR',
'ASSOCIATE EDITOR', 'SPORTS EDITOR', 'EDITOR THE DAILY', ]

def get_archives_years():
    entries = os.listdir(ARCHIVES_TEXT_PATH)
    filtered = []
    for i in range(0, len(entries)):
        try: 
            filtered.append( int(entries[i]))
        except:
            continue
    return filtered

def get_archives_months(year):
    entries = os.listdir(ARCHIVES_TEXT_PATH + str(year).zfill(4) + "/")
    filtered = []
    for i in range(0, len(entries)):
        try: 
            filtered.append( int(entries[i]))
        except:
            continue
    return filtered

def get_archives_days(year, month):
    entries = os.listdir(ARCHIVES_TEXT_PATH + str(year).zfill(4) + "/" + str(month).zfill(2) + "/")
    filtered = []
    for i in range(0, len(entries)):
        try: 
            filtered.append( int(entries[i]))
        except:
            continue
    return filtered

def get_archives_article_filenames(year, month, day):
    entries = os.listdir(ARCHIVES_TEXT_PATH + str(year).zfill(4) + "/" + str(month).zfill(2) + "/" + str(day).zfill(2))
    return entries

"""
returns a dict containing article data
"""
def get_author_data(year, month, day, filename):
    with open(ARCHIVES_TEXT_PATH + str(year).zfill(4) + "/" + str(month).zfill(2) + "/" + str(day).zfill(2) + "/" + filename, 'r') as f:
        articleData = f.read()
        articleLines = articleData.splitlines()
        if(not articleLines[2].startswith('###')):
            print("error in third line of article", year, month, day, filename)
        author = articleLines[2][4:]
        return author

def main():
    total_seen = 0
    archives_years = get_archives_years()
    archives_years.sort()
    for year in archives_years[len(archives_years) - 25:]:
        print("\n\n\nYEAR", year, "\n\n\n")
        archives_months = get_archives_months(year)
        for month in archives_months:
            archives_days = get_archives_days(year, month)
            for day in archives_days:
                article_names = get_archives_article_filenames(year, month, day)
                for article in article_names:
                    authorname = get_author_data(year, month, day, article)
                    skip = 0
                    for known_title in KNOWN_TITLES:
                        if(authorname.upper().find(known_title) > 0):
                            skip = 1
                    if(skip == 0 and len(authorname.strip()) > 0):
                        parts = authorname.split(' ')
                        if(len(parts) > 3):
                            print(parts[2:])
                            total_seen += 1
                            if(total_seen > 1000):
                                return

if __name__ == '__main__':
    main()