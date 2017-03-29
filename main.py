import os
import pdf
import scipy.ndimage
import scipy.misc
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = "./output/"
MAPS_DIR = "./maps/"

id = 4807384937 #Change this for another file

map_18 = scipy.ndimage.imread("{}map_18.png".format(MAPS_DIR))
map_17 = scipy.ndimage.imread("{}map_17.png".format(MAPS_DIR))

filetypes = ["chamber_rest","chamber_stress","wall_rest","wall_stress"]

key_18 = [[50,0,0],[100,0,0],[150,0,0],[200,0,0],[250,0,0], [250,50,0], #Pixel colours for the key
          [0,50,0],[0,100,0],[0,150,0],[0,200,0],[0,250,0],[0,250,50],
          [0,0,50],[0,0,100],[0,0,150],[0,0,200],[0,0,250],[50,0,250]]

offsets_18 = {1: (16, 0), 2: (9, 9), 3: (-9, 9), 4: (-16, 0), 5: (-9, -9), 6: (9, -9), #How much to move each pixel by
              7: (12, 0), 8: (6, 6), 9: (-6, 6), 10:(-12, 0), 11:(-6, -6), 12:(6, -6),
              13:(8, 0), 14:(3, 3), 15:(-3, 3), 16:(-8, 0), 17:(-3, -3), 18:(3, -3),}

key_17 = [[50, 10, 0],  [50, 20, 0],  [50, 30, 0],  [50, 40, 0],  [50, 50, 0],  [50, 60, 0], #Pixel colours for the key
          [100, 10, 0], [100, 20, 0], [100, 30, 0], [100, 40, 0], [100, 50, 0], [100, 60, 0],
          [150, 10, 0], [150, 20, 0], [150, 30, 0], [150, 40, 0],
          [200, 00, 0]]

colours = [("red",200,255,0,50,'#fd0002'),
           ("redpink",200,255,50,150,'#f95353'),
           ("pink",200,255,150,220,'#f7a7a6'),
           ("white",220,255,220,255,'#ffffff'),
           ("lightblue",150,220,220,255,'#adbcfa'),
           ("blue",50,150,220,255,'#5b7df7'),
           ("darkblue",0,50,220,255,'#0641f4')] #Name, >= (red), <= (red), >= (blue), <= (blue), plotcolour

if not os.path.exists("{}{}/processing/chamber_rest.jpg".format(OUTPUT_DIR,id)):
    print("File not found, loading PDF")
    pdf.extract_jpg("{}".format(id))
else: print("File found")

def load_images():
    files = []
    for file in filetypes:
        inputfile = scipy.ndimage.imread("{}{}/processing/{}.jpg".format(OUTPUT_DIR,id,file))
        files.append((file,inputfile,np.zeros(inputfile.shape),np.zeros(inputfile.shape)))
    return files

def segment_score():
    segment_score = []
    for name,input,output_processing,output in load_images():
        segment_score_image = [[0]*len(colours) for n in range(17)]
        for y in range(input.shape[0]):
            for x in range(input.shape[1]):
                if np.ndarray.tolist(map_18[y,x][:-1]) in key_18: #If colour of current pixel on map_18; based on result...
                    seg = key_18.index(np.ndarray.tolist(map_18[y,x][:-1])) + 1
                    output_processing[y+offsets_18[seg][0],x+offsets_18[seg][1]] = input[y,x] #...Then write the pixel and move based on location
        scipy.misc.imsave("{}{}/processing/{}-output-processing.png".format(OUTPUT_DIR,id,name),output_processing)
        for y in range(input.shape[0]): #We use a second loop because the above loop is writing to pixels on several rows below or above
            for x in range(input.shape[1]):
                if np.ndarray.tolist(map_17[y, x]) != [0, 0, 0, 0]: #If the segment isn't black in the map it must be a segment of interest
                    output[y, x] = output_processing[y, x]
                    if np.ndarray.tolist(map_17[y, x][: -1]) in key_17: #If the pixel colour in the map is actually one of the colours we care about (rather than antialiased crap...)
                        image_pixel = np.ndarray.tolist(output[y,x])
                        segment = key_17.index(np.ndarray.tolist(map_17[y, x][: -1]))
                        for cid,colour in enumerate(colours):
                            if (colour[1] <= image_pixel[0] <= colour[2]) and (colour[3] <= image_pixel[2] <= colour[4]):
                                segment_score_image[segment][cid] += 1
        scipy.misc.imsave("{}{}/{}-output.png".format(OUTPUT_DIR, id, name), output)
        segment_score.append(segment_score_image)
    return segment_score

def barplot(scores):
    print(scores)
    n = len(scores)
    ind = np.arange(n)
    width = 0.1
    fig, ax = plt.subplots()
    for cid,colour in enumerate(colours):
        pixcount = np.array([a[cid] for a in scores])
        pixtotal = np.array([sum(a) for a in scores])
        ax.bar(ind+width*cid, pixcount/pixtotal, width, color=colour[5])
    ax.set_ylabel('Number of pixels')
    ax.set_title('Pixel distribution')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(range(1,n+1))
    plt.show()

def savescores(scores):
    for i,image in enumerate(scores):
        csv = "segment,red,redpink,pink,white,lightblue,blue,darkblue"
        for s,segment in enumerate(image):
            csv = csv+"\n{},".format(s+1)
            for colour in segment:
                csv = csv+"{},".format(colour)
        with open("{}{}/{}.csv".format(OUTPUT_DIR,id,filetypes[i]), "w") as csv_file:
            csv_file.write(csv)

def main():
    scores = segment_score()
    savescores(scores)
    for score in scores:
        barplot(score)

main()