#Adapted from https://nedbatchelder.com/blog/200712/extracting_jpgs_from_pdfs.html

import os

def extract_jpg(filename):
    startmark = b"\xff\xd8"
    startfix = 0
    endmark = b"\xff\xd9"
    endfix = 2
    i = 0
    INPUT_DIR = "./input/"
    OUTPUT_DIR = "./output/"
    SAVED_IMAGES = {7:'wall_rest',9:'wall_stress',11:'chamber_rest',13:'chamber_stress'}


    with open("{}{}.pdf".format(INPUT_DIR,filename), "rb") as f:
        pdf = f.read()

    if not os.path.exists(OUTPUT_DIR + filename):
        os.makedirs(OUTPUT_DIR + filename)
        os.makedirs(OUTPUT_DIR + filename + "/processing")

    njpg = 0
    while True:
        istream = pdf.find(b"stream", i)
        if istream < 0:
            break
        istart = pdf.find(startmark, istream, istream + 20)
        if istart < 0:
            i = istream + 20
            continue
        iend = pdf.find(b"endstream", istart)
        if iend < 0:
            raise Exception("Didn't find end of stream!")
        iend = pdf.find(endmark, iend - 20)
        if iend < 0:
            raise Exception("Didn't find end of JPG!")

        istart += startfix
        iend += endfix
        jpg = pdf[istart:iend]
        if njpg in SAVED_IMAGES:
            with open("{}{}/processing/{}.jpg".format(OUTPUT_DIR,filename,SAVED_IMAGES[njpg]), "wb") as jpgfile:
                jpgfile.write(jpg)

        njpg += 1
        i = iend

