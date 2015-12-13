# pdf-utils
A utility to handle commonly done PDF related tasks..

## Usage

### PDF Joining

pdf-utils will enable you to join a directory of PDFs into a singe large pdf.

To use this feature you run the command:

 `./pdf-utils join myPdfDirectory/ largepdf.pdf`

### Password Removal
To Be Added

### Watermarking
To Be Added

## Linux/OS X Installation (Setup)

0. Create a directory to set up virtualenv and code.
  * Run the command `mkdir pdf-utils`
1. Create a virtual environment using virtualenv and python3
  * Run the command `virtualenv -p python3 pdf-utils`
2. Enter and activate the newly created directory.
 * Run the command `cd pdf-utils`
 * Run the command `source bin/activate`
3. Acquire pdf-utils
  * Run the command `git clone https://github.com/mholiv/pdf-utils.git`
4. Install the dependencies in the virtual environment.
  * Run the command `pip install click pypdf2`
5. Mark 'pdf-utils' as executable.
  * `chmod +x pdf-utils`



## Requirements
0. Python 3.x
1. Python package `virtualenv`
2. Python package `click`
3. Python package `pypdf2`
