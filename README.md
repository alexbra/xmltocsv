XML to CSV custom parser. Convert document paragraphs and chapters of technical and law documentation into csv table.
There are regulatory documents and rules stored in XML and DOCX files to teaching 100,000 more employees.
All files need to be moved into corporate learninig portal to build more convinient learning and testing system.
Each regulatory document (book.xml) matched to another XML document (questions.xml) contained testing questions for each paragraph. Need to convert all documents into csv mediator files to further import them into learning management system.

`xmltocsv.py` convert XML files into the following:

- `parts.csv` documents structure

|book_id|book_name|name|code|parent_code|type|url|paragraphs|
|:----|:----|:----|:----|:----|:----|:----|:----|
|book_332|332. Book|2. Chapter|1298385727632_34|				|folder|../protec_book_332/content/1298385727632_34.html| |
|book_332|332. Book|          |1298385727632_35|1298385727632_34|lesson|../protec_book_332/content/1298385727632_35.html|1298385727632_36^1298385727642_38^1298385727642_39|

- `questions.csv` testing questions

|bookcode|partcode|qcode|qname|type|is_correct|answname|bookname|partname|group|
|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|
|book_332|1298385727632_35|1298385727632_18_2|Name of question|multiple_choice|1|answer|332. Book|part name|coll_2008|

- `contetnt` (folder) contained HTML files with document's content

`docxtocsv.py` create similar csv and html files from DOCX source.  



