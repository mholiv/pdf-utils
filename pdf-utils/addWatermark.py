from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import io
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
import multiprocessing
from multiprocessing import Pool


def _worker(pdfSet):
    """The worker pdf typically called to work on a pool. It expects to receive
    a dictionary with the following keys: 'message', 'start', 'data' and 'end'.
    Message should be a string that will be watermarked on the page. Start
    should be the first page this worked should begin with and end should be the
    final page this worker will work on. This function returns a bytesIO object
    that is the output of PdfFileWriter()"""

    #First we set our variables
    inputdoc = PdfFileReader(pdfSet['data'])
    outputFile = PdfFileWriter()
    start = pdfSet['start']
    end = pdfSet['end']

    #In some cases we may allocate extra pages to be processed beyond the pdf
    #page count. Here we address that. It's messy I know.
    for pageNumber in range(start,end+1):
        try:
            inputdoc.getPage(pageNumber)
        except IndexError:
            break

        #We get the size of the pdf so we can center the watermark later
        x = inputdoc.getPage(pageNumber).mediaBox[2]
        y = inputdoc.getPage(pageNumber).mediaBox[3]

        #We format the layout of the watermark. For now just top and bottom
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(x,y))
        c.setFont('Courier', 8)
        c.setFillColorRGB(128/255,128/255,128/255)

        #We create a blank pdf page and lay out our watermark
        textWidth = stringWidth(pdfSet['message'], 'Courier', 8)
        horLoc = (float(x) - textWidth) / 2
        virLoc = float(y) - 8
        c.drawString(horLoc,5,pdfSet['message'])
        c.drawString(horLoc,virLoc,pdfSet['message'])
        c.save()
        packet.seek(0)

        #In some cases watermarks will not appear on PDF we overlay the marks
        #'above' and 'below' the original content to ensure it will show up.
        #We then merge our watermark pdfs and our original content.
        newpage1 = PdfFileReader(packet).getPage(0)
        newpage = PdfFileReader(packet).getPage(0)
        newpage.mergePage(inputdoc.getPage(pageNumber))
        newpage.mergePage(newpage1)
        outputFile.addPage(newpage)

    #We write out pdf to a BytesIO object and return it.
    returnBuffer = io.BytesIO()
    outputFile.write(returnBuffer)
    return(returnBuffer)



def waterMark(inputPdfLocation,outputPdfLocation,waterString):
    """This fuction takes three arguments a input pdf location, an output pdf
    location, and a string that will be watermarked. This fuction will process
    the PDF add a watermark, then write the file to the output location

    =======WARNING: THIS FUNCTION CRASHES UPON RECIEVING VERY LARGE PDFS========

    """

    #create an object to hold result pages
    try:
        raw =open(inputPdfLocation,"rb")
        rawPdf = io.BytesIO(raw.read())
        inputdoc = PdfFileReader(rawPdf)
    except Exception as e:
        print(e)
        print('Did you input a valid PDF file?')
        return 1


    #We set the amount of workers
    pageCount = inputdoc.getNumPages()

    if multiprocessing.cpu_count() > pageCount:
        workers = pageCount
    else:
        workers = multiprocessing.cpu_count()
    floorNum = pageCount//workers
    workingSplitNumber = pageCount-1


    #We split the pdf pages into even groups
    splits = []
    startNum = 0
    endNum = 0
    while workingSplitNumber >= 1:

        endNum = endNum + floorNum
        workingSplitNumber = workingSplitNumber - floorNum
        splits.append({'start':startNum,
                        'end':endNum,
                        'data':rawPdf,
                        'message':waterString})
        startNum = endNum + 1


    #Create the pool and process the data
    pool = Pool(processes=workers)
    pdfBinaryList =  pool.map(_worker, splits)


    #Re recombine the marked pages in a new single PDF
    masterPdf = PdfFileMerger()
    for pBinary in pdfBinaryList:
        pdfSegment = PdfFileReader(pBinary)
        #Do not try to combine these two. It will lead to stack over
        masterPdf.append(pdfSegment)


    #We write the PDF to the drive.
    outputFile = PdfFileWriter()
    outputStream = open(outputPdfLocation,"wb")
    masterPdf.write(outputStream)
    outputStream.close()
