"""
Runs corrections from Veridian and applies them to the text files.
Usage:
    wget [FILE URL] 
    tar -xf stanford-text-corrections-20190513.tar.gz
    python3 -m pip install tqdm 
    python3 corrections.py 
"""
import xml.etree.ElementTree as ET
import os
import re
import fileinput
from tqdm import tqdm

PATH = "./stanford-text-corrections/stanford"
LOCATION = "./output"
def create_corrections():
    years = os.listdir(PATH)
    for year in filter(lambda x: os.path.isdir(os.path.join(PATH, x)), years):
        for directory in os.listdir(os.path.join(PATH, year)):
            for (dirname, year, month, day) in re.findall(r'((\d{4})(\d{2})(\d{2})-\d{2})', directory):
                tqdm.write(dirname) 
                path = os.path.join(PATH, year, dirname + ".dir", f"stanford{dirname}-changes.log")
                with open(path) as f:
                    xml = f.read()
                tree = ET.fromstring("<root>" + xml + "</root>")
                # print(tree, year, month, day)
                corrections = []
                files = [os.path.join(LOCATION, year, month, day, file) for file in os.listdir(os.path.join(LOCATION, year, month, day))]
                print("files", files) 
                for textCorrectedBlock in tree:
                    blockID = textCorrectedBlock.attrib["blockID"]
                    corrections = {} 
                    for textCorrectedLine in textCorrectedBlock:
                        oldTextValue = textCorrectedLine.findtext("OldTextValue").strip()
                        newTextValue = textCorrectedLine.findtext("NewTextValue").strip()
                        corrections[oldTextValue] = newTextValue
                if len(corrections) > 0: 
                    yield files, corrections

for files, corrections in tqdm(create_corrections()):
    for file in files:
        print(file)
        with open(file, "r") as f:
            lines = f.readlines()
        with open(file, "w") as f:
            for line in lines:
                if line.strip() in corrections:
                    f.write(corrections[line.strip()] + "\n")
                else:
                    f.write(line)
