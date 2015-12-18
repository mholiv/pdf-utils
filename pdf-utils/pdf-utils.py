#!/usr/bin/env python
__author__ = "Caitlin Campbell"
__copyright__ = "Copyright 2015, Caitlin Campbell"
__license__ = "AGPL 3"
__version__ = "1.0.0"

import os
import click
from joinpdf import multiprocesPdfs
from addWatermark import waterMark

@click.group()
def cli():
    pass

@cli.command()
@click.argument('argss', nargs=2)
def watermark(argss):
    # First move to working directory. That way relative paths will work.
    os.chdir(os.getcwd())

    #Get your source directory and output.
    inputPdf = os.path.abspath(argss[0])
    outputPdf = argss[1]

    #Add absolute path to out if needed.
    if outputPdf[0] != ('/' or '~'):
        outputPdf = os.path.join(os.getcwd(),outputPdf)

    #Do the actual watermarking
    waterMark(inputPdf,outputPdf)



@cli.command()
@click.argument('argss', nargs=2)
def join(argss):

    # First move to working directory. That way relative paths will work.
    os.chdir(os.getcwd())

    #Get your source directory and output.
    directory = os.path.abspath(argss[0])
    output = argss[1]

    #Verify that directory exists and contains one PDF put those verified PDFs \
    #in a list
    pdfList = []
    try:
        files = os.listdir( directory )
        for filee in files:
            if filee[-4:] == '.pdf':
                pdfList.append(filee)
    except:
        print('Could not find directry or directory has no pdfs')
        pdfList = []

    #If the first character in the directory is a '/' we know it is an absolute
    #directory else we add the absolute path. I know c style loops are not very
    #'python-esque' but python loops don't allow for in place editing.
    i = 0
    for i in range(len(pdfList)):
        if pdfList[i][0] != ('/' or '~'):
            pdfList[i] = os.path.join(directory,pdfList[i])

    #Add absolute path to out if needed.
    if output[1] != ('/' or '~'):
        output = os.path.join(os.getcwd(),output)

    # Call actual function to do the work.
    multiprocesPdfs(pdfList,output)




if __name__ == '__main__':
    cli()
