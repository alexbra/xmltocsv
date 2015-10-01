import mammoth
from BeautifulSoup import BeautifulSoup
import pandas as pd
import os

def makeDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def createHtml(folderName, part, html):
    filename = folderName+'/content/'+part+'.html'
    with open(filename,'w') as html_file:
        html_file.write(html)
        
def convert_image(image):
    with image.open() as image_bytes:
        encoded_src = base64.b64encode(image_bytes.read()).decode("ascii")

    return {
        "src": "data:{0};base64,{1}".format(image.content_type, encoded_src)
    }

with open("ll.docx", "rb") as docx_file:
    result = mammoth.convert_to_html(docx_file)
    html = result.value
    counter = 100001
    soup = BeautifulSoup(html)
    table = soup.find('table')
    trs = table.findAll('tr', recursive=False)
    book_code = 'protec_book_' + trs[0].findAll('td')[1].text
    code = str(trs[0].findAll('td')[1].text)+'_'+str(counter)
    book_number = trs[0].findAll('td')[1].text
    book_name = trs[3].findAll('td')[1].text
    book_desc = "".join([str(x) for x in trs[3].findAll('td')[2].contents])
    
    name = book_name
    if trs[3].findAll('td')[2].text == '':
        _type = 'folder'
        url = ''
    else:
        _type = 'lesson'
        url = '../'+book_code+'/content/'+code+'.html'

    parent_code = ''
    
    book_ids = []
    book_names = []
    names = []
    codes = []
    parent_codes = []
    types = []
    urls = []

    _path = book_code+'\\content'
    makeDirectory(_path)
    createHtml(book_code, code, book_desc)
   
    book_ids.append(book_code)
    book_names.append(book_name.encode("utf-8"))
    names.append(name.encode("utf-8"))
    codes.append(code)
    parent_codes.append(parent_code)
    types.append(_type)
    urls.append(url)
    cur_parent_1 = ''
    cur_parent_2 = ''
    cur_parent_3 = ''    
    
    for tr in trs[4:]:
                
        counter += 1
        tds = tr.findAll('td')
        code = book_number+'_'+str(counter)
        
        name = tr.findAll('td')[1].text
        if tr.findAll('td')[2].text == '':
            _type = 'folder'
            url = ''
        else:
            _type = 'lesson'
            book_desc = "".join([str(x) for x in tr.findAll('td')[2].contents])
            book_desc = book_desc.replace("<p>", "<p>"+str(name)+" ",1)
            url = '../'+book_code+'/content/'+code+'.html'
            createHtml(book_code, code, book_desc)

        if int(tr.findAll('td')[0].text) == 1:
            cur_parent_1 = code
            parent_code = ''
        elif int(tr.findAll('td')[0].text) == 2:
            cur_parent_2 = code
            parent_code = cur_parent_1
        elif int(tr.findAll('td')[0].text) == 3:
            cur_parent_3 = code
            parent_code = cur_parent_2
        else:
            cur_parent_4 = code
            parent_code = cur_parent_3
            
 
        book_ids.append(book_code)
        book_names.append(book_name.encode("utf-8"))
        names.append(name.encode("utf-8"))
        codes.append(code)
        parent_codes.append(parent_code)
        types.append(_type)
        urls.append(url)

    
    preds = pd.DataFrame({"book_id": book_ids, "book_name": book_names, "name": names, "code": codes, "parent_code": parent_codes, "type": types, "url": urls})
    preds = preds[['book_id','book_name','name','code','parent_code','type','url']]
    preds.to_csv('docxparts.csv', index=False)
    

