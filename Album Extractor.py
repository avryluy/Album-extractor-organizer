import time as time
import pathlib as path
import shutil as sht


#Declare Downloads path
downloadPath = path.Path(r"C:\Users\avryl\Downloads\AlbumExtractor")
#Declare music library path
musicLibrary = path.Path(r"C:\Users\avryl\Music")
downloadFolder = str(downloadPath)
#Store zip type in a variable
zipSuffix = ".zip"

def pathStatSize(x):
    pathSize = x.stat().st_size
    return pathSize 

#Check for zip files. Determine how many there are.
def zipCounter():
    count = 0
    for child in downloadPath.iterdir():
        childstype = child.suffix
        if childstype == ".zip":
            count += 1
        else: count += 0
        #splice zip name to get Artist
        print(child.name.split(".")[0])
        #store zip path in a variable
        childPath = downloadPath / child
        # print(childPath)
    if  count == 1:
        print("There is 1 zip to be unpacked.")
    elif count == 0:
        print("There are no zips to be unpacked.")
    else:
        print("There are {} zips to be unpacked.".format(count))


def zipManager():
    for child in downloadPath.iterdir():
        if child.match("*.zip") == True:
            #store zip path in a variable
            childPath = downloadPath / child
            print(childPath)
            #Unpack the zipfile into a directory of the zips name
            sht.unpack_archive(childPath,downloadPath,"zip")
            print("Album Extracted")
            folderName = child.name.split(".")[0]
            #splice zip name to get Artist, store in variable
            artistName = folderName.split(" - ")[0]
            #splice zip name to get album name, store in variable
            albumName = folderName.split(" - ")[1]
            #capture path of extracted folder
            extractFolder = downloadPath / folderName
            print("******")
            #Capture Music Library Artist Path
            artistPath =  musicLibrary / artistName
            #Check if artist folder exists
            artistCheck = artistPath.exists()
            if artistCheck == False:
                print("Artist directory doesn't exist. Creating...")
                #Create Artist folder if it doesn't exist
                artistPath.mkdir()
                print("Done.")
            #Capture Music Library Album Path
            albumPath = artistPath / albumName
            #check if album exists
            albumCheck = albumPath.exists()
            #For each zip, Check music library for directory of the album name. Return bool
            if albumCheck == False:
                print("Moving files...")
                #Move new directory in Artist directory
                sht.move(extractFolder, albumPath)
                print("Done.")
            #If album folder exists but is empty, populate it with files.
            elif albumCheck == True and (pathStatSize(albumPath) == 8192 or pathStatSize(albumPath) == 0):
                print("Folder exists but nothing is inside. Copying...")
                sht.copytree(extractFolder, albumPath, dirs_exist_ok=True)
                print("Done.")
            else:
                #Return "Album already exists."
                print("Album already exists here.")
                
zipCounter()
print("******")
zipManager()

#iterate over files to strip Artist + Album name from file name. LEAVE TRACK NUMBER

#delete zip file in downloads folder

#Return "Directory created."
#Ask to open location
#*IF YES* Open location and exit program
#*IF NO* Exit program 

#***IF TRUE***



#Ask to if files should be deleted?

#*IF YES* delete new directory with files

#*IF NO* Exit program