# -*- coding: cp1251 -*-
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import os


def makeDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def getParts(bookCode,courseName,listNodes,parentCode,nodeType):
    global arrParts   
    for el in listNodes:
           paragraphs = ''
           
           if nodeType == 'slice':
               name_node = el.findall('MARKER')[0].text
           else:
               name_node = el.findall('TITLE')[0].text

           code = el.get("ID")
           parent_code = code
           
           childNodes = el.findall("NODE")
           
           node_type = 'node'
           
           if len(childNodes)==0:
               childNodes = el.findall("SLICE")
               node_type = 'slice'
               
           if len(childNodes)==0:
               _type = 'lesson'
               paragraphs = getParagraphIDs(el)
           else:
               _type = 'folder'
           
           arrParts.append( {
               'book_id':bookCode,
               'book_name':courseName.encode("utf-8"),
               'code': code.encode("utf-8"),
               'parent_code': parentCode.encode("utf-8"),
               'type': _type.encode("utf-8"),
               'url': '../'+bookCode+'/content/'+code+'.html',
               'name': name_node.encode("utf-8"),
               'paragraphs': paragraphs
           })

           
           if len(childNodes)>0:
               getParts(bookCode, courseName,childNodes,parent_code,node_type)

def getParagraphIDs(elem):
    paragraphElementsIDsrt = ''
    paragraphElementsArray = elem.findall(".//*/PARAGRAPH")
    if len(paragraphElementsArray) > 0:
        paragraphElementsIDsrt = "^".join([el.get("ID") for el in paragraphElementsArray ])
    return paragraphElementsIDsrt

def createCSV(output_file):
    global arrParts;
    with open(output_file,'w') as master_file:
       master_file.write('book_id;book_name;name;code;parent_code;type;url;paragraphs\n')
       for part in arrParts:
           master_file.write(part['book_id']+';'+part['book_name']+';'+part['name']+';'+part['code']+';'+part['parent_code']+';'+part['type']+';'+part['url']+';'+part['paragraphs']+'\n')

def getChildHtml(nodeID):
    global body
    htmlStr = '<pre>'
    arrChildNodes = body.findall(".//*[@ID='"+nodeID+"']//")
    for part in arrChildNodes:
        if part.tag == 'PARAGRAPH' or part.tag == 'LINE':
            htmlStr +='<br>'
        
        if part.tag=='TEXT' or  part.tag=='INTLINK':
            htmlStr += part.text.encode("utf-8")
        
    htmlStr += '</pre>'
    return htmlStr

def createHtml(listCodes, folderName):
    global body
    _path = folderName+'\\content'
    makeDirectory(_path)
    for part in listCodes:
        htmlStr = ''
        filename = folderName+'/content/'+part+'.html'
        arrChildNodes = body.findall(".//*[@ID='"+part+"']")
        htmlStr += getChildHtml(part)
        with open(filename,'w') as html_file:
            #print arrChildNodes
            #htmlStr+=str(part)
            html_file.write(htmlStr)

def getAnswers(elem):
    global arrQuestions, arrParts, book_name
    answersElementsArray = elem.findall("./ANSWERS/SELECT_ANSWER")
    correctArray = elem.findall("./ANSWERS/SELECT_ANSWER/IS_CORRECT")
    countCorrectAnsw = len([item for item in correctArray if item.text == '1'])
    
    if countCorrectAnsw>1:
        question_type = 'multiple_response'
    else:
        question_type = 'multiple_choice'
    #Определить какой код будет у вопроса. Код равен коду раздела part из массива arrParts, в котором есть совпадение в столбце paragraphs с DOC_REF ID текущего вопроса 

    docrefid = elem.find("DOC_REF/ID").text
    qname = elem.find("TEXT").text
    partcode = ''
    for item in arrParts:
        if docrefid in item['paragraphs']:
            partcode = item['code']
            partname = item['name']
    
    if partcode!='':
        qcode = partcode+'_'+elem.get("ID")    
        #print qcode, elem.find("TEXT").text, countCorrectAnsw
        for el in answersElementsArray:
            answer_name = el.find("./TEXT").text
            is_correct = el.find("./IS_CORRECT").text
            arrQuestions.append( {
                'bookcode':book_code,
                'partcode':partcode,
                'qcode':qcode,
                'qname':qname.replace(';', ',').encode("utf-8"),
                'question_type': question_type,
                'is_correct': is_correct,
                'answer_name': answer_name.replace(";", ",").encode("utf-8"),
                'book_name': book_name.replace(";", ",").encode("utf-8"),
                'part_name': partname.replace(";", ",") #encode не нужно делать в случае ошибки кодировки.           
            })    

def getQuestions(itemsTree):
    questionsElementsArray = itemsTree.findall("./SELECT_ANSWER_QUESTION")
    for el in questionsElementsArray:
        getAnswers(el)

def createQuestionsCSV(output_file):
    global arrQuestions
    with open(output_file,'w') as master_file:
       master_file.write('bookcode;partcode;qcode;qname;type;is_correct;answname;bookname;partname;group\n')
       for part in arrQuestions:
           master_file.write(part['bookcode']+';'+part['partcode']+';'+part['qcode']+';'+part['qname']+';'+part['question_type']+';'+part['is_correct']+';'+part['answer_name']+';'+part['book_name']+';'+part['part_name']+';coll_2008\n')
           
    



dir = 'c:\\pyth\\xmltocsv\\books'

for el in next(os.walk(dir))[1]:
    arrParts = []
    arrQuestions = []
    path_book = dir +'\\'+el+'\\Book.xml'
    path_questions = dir +'\\'+el+'\\Questions.xml'
    
    tree = ET.parse(path_book)
    qtree = ET.parse(path_questions)


    root = tree.getroot()
    body = root.find("BODY")
    header = root.find("HEADER")
    book_code = 'protec_book_'+header.find("CODE").text
    book_name = header.find("TITLE").text
    qroot = qtree.getroot()
    qitems = qroot.find("ITEMS")


    names = body.findall('NODE')

    getParts(book_code, book_name, names, '','node')    
    createCSV('parts.csv')

    lessonParts = []
    for item in arrParts:
        if item['type'] == 'lesson':
            lessonParts.append(item['code'])

    createHtml(lessonParts, book_code)

    getQuestions(qitems)
    createQuestionsCSV('questions.csv')
