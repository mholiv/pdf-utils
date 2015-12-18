from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import io
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize
from reportlab.pdfgen import canvas
import multiprocessing
from multiprocessing import Pool
import base64


def _worker(pdfSet):
    inputdoc = PdfFileReader(pdfSet['data'])
    outputFile = PdfFileWriter()
    start = pdfSet['start']
    end = pdfSet['end']




    print(start,end)
    for pageNumber in range(start,end+1):
        print(pageNumber)

        x = inputdoc.getPage(pageNumber).mediaBox[2]
        y = inputdoc.getPage(pageNumber).mediaBox[3]

        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(x,y))
        c.setFont('Times-Italic', 8)
        c.setFillColorRGB(128/255,128/255,128/255)


        textWidth = stringWidth(pdfSet['message'], 'Times-Italic', 8)
        horLoc = (float(x) - textWidth) / 2
        virLoc = float(y) - 8
        c.drawString(horLoc,5,pdfSet['message'])
        c.drawString(horLoc,virLoc,pdfSet['message'])
        c.save()
        packet.seek(0)

        newpage1 = PdfFileReader(packet).getPage(0)
        newpage = PdfFileReader(packet).getPage(0)
        newpage.mergePage(inputdoc.getPage(pageNumber))
        newpage.mergePage(newpage1)
        outputFile.addPage(newpage)

    returnBuffer = io.BytesIO()
    outputFile.write(returnBuffer)
    return(returnBuffer)



def waterMark(inputPdfLocation,outputPdfLocation):

    #create an object to hold result pages
    raw =open(inputPdfLocation,"rb")
    rawPdf = io.BytesIO(raw.read())
    inputdoc = PdfFileReader(rawPdf)
    #base85pdf = base64.b85encode(rawPdf.getvalue())

    #THIS NEEDS REPLACED ASAP
    date = "Jul 18, 2015"
    email = "caitlin@cissols.com"
    name = "Caitlin Campbell"
    accoutNum = "2474565"
    tString = "paizo.com #{0}, {1} <{2}>, {3}".format(accoutNum,name,email,date)


    pageCount = inputdoc.getNumPages()


    if multiprocessing.cpu_count() > pageCount:
        workers = pageCount
    else:
        workers = multiprocessing.cpu_count()

    floorNum = pageCount//workers

    workingSplitNumber = pageCount-1



    splits = []

    startNum = 0
    endNum = 0

    while workingSplitNumber >= 1:

        endNum = endNum + floorNum
        workingSplitNumber = workingSplitNumber - floorNum
        splits.append({'start':startNum,
                        'end':endNum,
                        'data':rawPdf,
                        'message':tString})
        startNum = endNum + 1


    print(splits)



    #Create the pool and process the data
    pool = Pool(processes=workers)
    pdfBinaryList =  pool.map(_worker, splits)


    masterPdf = PdfFileMerger()
    for pBinary in pdfBinaryList:
        pdfSegment = PdfFileReader(pBinary)

        print(pdfSegment.getNumPages())


        #Do not try to combine these tewo. It will lead to stack over
        masterPdf.append(pdfSegment)

    print(pdfBinaryList)
    outputFile = PdfFileWriter()
    outputStream = open(outputPdfLocation,"wb")
    masterPdf.write(outputStream)
    outputStream.close()
