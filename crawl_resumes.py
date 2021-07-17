#!/usr/local/bin/python3
import PyPDF2, docx, sys, re
from os import walk

RESUME_PATH = "/Users/aaron/Documents/Resume"
BUZZ_WORDS_FILE = "/Users/aaron/Scripts/buzzwords.txt"

buzzwords = []
with open(BUZZ_WORDS_FILE, 'r') as f:
    for line in f:
        buzzwords.append(line.strip())

resumes = next(walk(RESUME_PATH), (None, None, []))[2]  # [] if no file
if len(resumes) == 0:
    print("ERROR: no resumes found in path '{}'".format(RESUME_PATH))

for resume in resumes:
    buzzwords_found = []

    if resume.startswith('.'):
        continue # skip hidden files
    file_ext = resume.split('.')[-1]

    if file_ext in ['txt', 'doc', 'docx']:
        # resume is word doc
        doc = docx.Document(RESUME_PATH + '/' + resume)
        paras = [p.text for p in doc.paragraphs if p.text] 
        for para in paras:
            for word in re.split(' |,|\.|:|\(|\)|\;|-', para.lower()):
                for buzzword in buzzwords:
                    if buzzword.lower() == word.strip() and buzzword not in buzzwords_found:
                        buzzwords_found.append(buzzword)
        if len(buzzwords_found) > 0:
            buzzwords_found.sort()
            print("'{0}' buzzwords found: [{1}]".format(resume, ','.join(buzzwords_found)))
    elif file_ext in ['pdf']:
        # resume is pdf
        pdf = open(RESUME_PATH + '/' + resume, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdf)
        pages = pdfReader.numPages
        for n in range(0,pages):
            pageObj = pdfReader.getPage(n)
            text = pageObj.extractText().split("  ")
            for line in text:
                for word in re.split(' |,|\.|:|\(|\)|\;|-', line.lower()):
#                    print(word.strip())
                    for buzzword in buzzwords:
                        if buzzword.lower() == word.strip() and buzzword not in buzzwords_found:
                            buzzwords_found.append(buzzword)
        if len(buzzwords_found) > 0:
            buzzwords_found.sort()
            print("'{0}' buzzwords found: [{1}]".format(resume, ','.join(buzzwords_found)))
        pdf.close()
