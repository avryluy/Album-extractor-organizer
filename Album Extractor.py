import time as time
import pathlib as path
import shutil as sht

#Declare Downloads path
downloadFolder = path.Path(r"C:\Users\avryl\Downloads\AlbumExtractor")
#Declare music library path
musicLibrary = ""
#Check for zip files. Determine how many there are.
def zipCounter():
    count = 0
    for child in downloadFolder.iterdir():
            childstype = child.suffix
            if childstype == ".zip":
                count += 1
            else: count += 0
    if  count == 1:
        print("There is 1 zip to be unpacked.")
    elif count == 0:
        print("There are no zips to be unpacked.")
    else:
        print("There are {} zips to be unpacked.".format(count))

zipCounter()

#Store zip type in a variable

#store zip name in a variable

#splice zip name to get Artist, store in variable

#splice zip name to get album name, store in variable

#For each zip, Unpack the zipfile into a directory of the zips name
###path.mkdir

#For each zip, Check music library for directory of the album name. Return bool

#***IF FALSE***

#Move new directory in Artist directory

#iterate over files to strip Artist + Album name from file name. LEAVE TRACK NUMBER

#delete zip file in downloads folder

#Return "Directory created."
#Ask to open location
#*IF YES* Open location and exit program
#*IF NO* Exit program 

#***IF TRUE***

#Return "Album already exists."

#Ask to if files should be deleted?

#*IF YES* delete new directory with files

#*IF NO* Exit program