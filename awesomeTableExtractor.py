import pandas as pd
import numpy
import numpy as np
import os
from tabula import read_pdf
import PyPDF2
import pandas as pd
import requests
import sys

def fnPDF_FindText(xFile, xString,pageGreaterThan):
    # xfile : the PDF file in which to look
    # xString : the string to look for
    # pageGreaterThan : page offset
    import PyPDF2, re
    PageFound = -1
    pdfDoc = PyPDF2.PdfFileReader(open(xFile, "rb"))
    print('Number of pages:',pdfDoc.getNumPages())
    for i in range(pageGreaterThan, pdfDoc.getNumPages()):
        content = ""
        content += pdfDoc.getPage(i).extractText() + "\n"
        content1 = content.encode('ascii', 'ignore').lower()
        #print(str(content1))
        ResSearch = re.search(xString.lower(), str(content1))
        if ResSearch is not None:
            PageFound = i
            print('page found',i)
            print('Getting content!')
            break
    return PageFound,True
def didFind(xFile, xString,pageGreaterThan):
    # xfile : the PDF file in which to look
    # xString : the string to look for
    # pageGreaterThan : page offset
    import PyPDF2, re
    PageFound = False
    pdfDoc = PyPDF2.PdfFileReader(open(xFile, "rb"))
    print('Number of pages:',pdfDoc.getNumPages())
    for i in range(pageGreaterThan, pdfDoc.getNumPages()):
        content = ""
        content += pdfDoc.getPage(i).extractText() + "\n"
        content1 = content.encode('ascii', 'ignore').lower()
        #print(str(content1))
        ResSearch = re.search(xString.lower(), str(content1))
        if ResSearch is not None:
            print('Found More Pages')
            return True
    return False
def saveToPDF(xFile, xString,save_as):
    page = fnPDF_FindText(xFile, xString)
    pfr = PyPDF2.PdfFileReader(open(xFile, "rb")) #PdfFileReader object
    pg3 = pfr.getPage(page) #extract pg page
    
    writer = PyPDF2.PdfFileWriter() #create PdfFileWriter object

    #add pages
    writer.addPage(pg3)

    #filename of your PDF/directory where you want your new PDF to be
    NewPDFfilename = "New.pdf" 

    with open(NewPDFfilename, "wb") as outputStream: #create new PDF
        writer.write(outputStream) #write pages to new PDF
    df = read_pdf('New.pdf',multiple_tables=True)
    length = range(len(df))
    for i in length:
        data  = pd.DataFrame(df[i])
        data.to_csv(str(i)+save_as)

def fromURL(url,xString,save_as,pageGreaterThan = 0):
    response = requests.get(url)
    with open('storage/metadata.pdf', 'wb') as f:
        f.write(response.content)
        f.close()
    
    page,didfind = fnPDF_FindText('storage/metadata.pdf', xString,pageGreaterThan)
    print(page,didfind)
    metadata = open('storage/metadata.pdf', "rb")
    pfr = PyPDF2.PdfFileReader(metadata) #PdfFileReader object
    
    '''While loop goes here'''
    while(didFind('storage/metadata.pdf', xString,page)):
        
        print(didFind('storage/metadata.pdf', xString,page))
        #print('true')
        print(page)
        
        pg3 = pfr.getPage(page) #extract pg page, pg3 is the page number where the string is matched

        writer = PyPDF2.PdfFileWriter() #create PdfFileWriter object

        #add pages
        writer.addPage(pg3)

        #filename of your PDF/directory where you want your new PDF to be
        NewPDFfilename = "New.pdf" 
        print('Writing this page to csv')
        with open(NewPDFfilename, "wb") as outputStream: #create new PDF
            writer.write(outputStream) #write pages to new PDF
        df = read_pdf('New.pdf',multiple_tables=True)
        length = range(len(df))
        for i in length:
            data  = pd.DataFrame(df[i])
            data.to_csv(save_as +'/'+'page_'+str(page)+'table_'+str(i)+save_as+'.csv',index = False)
        page+=1
        print('0____________________________________________________________________________________________________0')
    metadata.close()
    print('finished')
       
def remove():
    os.remove('storage/metadata.pdf')

def main():
    url = input('Enter the url')
    string = input('Give the string you want to match. (e.g. Profit and loss statement).')
    filename = input('Give the filename to save the table.')
    offset = int(input('Page offset. Default starts at 0.' ) or '0')
    print('the filename is' + filename)
    os.mkdir(filename)
    fromURL(url,string,filename,offset)
    print('0____________________________________________________________________________________________________0')
    print('Dont forget to run python remove.py')
    print('0____________________________________________________________________________________________________0')
    print('SORRY FOR THE BUGS ;(')

if __name__ == "__main__":main() ## with if
