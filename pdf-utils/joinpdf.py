import multiprocessing
from multiprocessing import Pool
from PyPDF2 import PdfFileReader, PdfFileMerger

#Worker for the pool.
def _worker(pdf):
    """This function is a worker function that is meant to be used by the pool
    below. It takes a absolute PDF file location and returns a dictionary with
    the keys 'status', 'fileName', and 'byteCode'. Status is either true or
    false, depending on if the file was able to be read into byte code.
    Filename is the name of the file. Bytecode is the bytecode for the pdf"""
    try:
        pdf_byteCode = PdfFileReader(pdf, "rb")
        return({'status':True,'fileName':pdf,'byteCode':pdf_byteCode})
    except Exception as e:
        return((False,None))

def multiprocesPdfs(pdfList,output):
    """This function takes two arguments. The first is a directory containing a
    list of absolute pdf file locations. The second is the output file name.
    This should also be specified in absolute terms.

    This function will, using all avliable CPUs get the pdfs and join them into
    a single large pdf at the output location."""

    #We set the workers to the cpu core count or the pdf file count, whatever
    #is lower. That way we are never wasting reasources.
    if multiprocessing.cpu_count() > len(pdfList):
        workers = len(pdfList)
    else:
        workers = multiprocessing.cpu_count()

    #Create the pool and process the data
    pool = Pool(processes=workers)
    pdfBinaryList =  pool.map(_worker, pdfList)


    #Create the PDF File Merger Instance
    masterPdf = PdfFileMerger()

    #Warn if files are not processed, else add them to master pdf and write
    #the file out.
    for pdfBinary in pdfBinaryList:
        if pdfBinary['status'] != True:
            print('Could not process %s'% pdfBinary['fileName'])
        else:
            masterPdf.append(pdfBinary['byteCode'])
    masterPdf.write(output)
