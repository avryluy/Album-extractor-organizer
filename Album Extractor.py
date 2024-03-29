import pathlib as path
import shutil as sht
import os as os

# Declare Downloads path
downloadPath = path.Path(r"path/to/directory")
# Declare music library path
musicLibrary = path.Path(r"path/to/directory")
downloadFolder = str(downloadPath)
# Store zip type in a variable
zipSuffix = ".zip"
# Declare audio extensions
audioExtension = (".wav", ".mp3", ".aac", ".flac", ".ogg", ".alac", ".aiff")


def pathStatSize(x):
    xDir = os.listdir(x)
    pathSize = len(xDir)
    return pathSize

# Check for zip files. Determine how many there are.


def zipCounter(zipCountPath):
    # global count 
    count = 0
    for child in zipCountPath.iterdir():
        childstype = child.suffix
        if childstype == ".zip":
            count += 1
        else:
            count += 0
        # splice zip name to get Artist
    if count == 1:
        print("There is 1 zip to be unpacked.")
    elif count == 0:
        print("There are no zips to be unpacked.")
    else:
        print("There are {} zips to be unpacked.".format(count))
    return count


def zipManager(zipManPath):
    for child in zipManPath.iterdir():
        if child.match("*.zip"):
            global folderName
            folderName = child.name.split(".")[0]
            # splice zip name to get Artist, store in variable
            global artistName
            artistName = folderName.split(" - ")[0]
            # splice zip name to get album name, store in variable
            global albumName
            albumName = folderName.split(" - ")[1]
            # capture path of extracted folder
            global extractFolder
            print("Evaluating {} by {}").format(albumName, artistName)
            extractFolder = downloadPath / folderName
            os.mkdir(extractFolder)
            # Capture Music Library Artist Path
            global artistPath
            artistPath =  musicLibrary / artistName
            # store zip path in a variable
            childPath = downloadPath / child
            # Unpack the zipfile into a directory of the zips name
            sht.unpack_archive(childPath,extractFolder,"zip")
            print("Album Extracted")
            # Check if artist folder exists
            artistCheck = artistPath.exists()
            # Create Artist folder if it doesn't exist
            if artistCheck is False:
                print("Artist directory doesn't exist. Creating...")
                artistPath.mkdir()
                print("Done.")
            # Capture Music Library Album Path
            global albumPath
            albumPath = artistPath / albumName
            # Create path for album folders that aren't cleaned up
            badFolderPath = artistPath / folderName
            # check if album exists
            albumCheck = albumPath.exists()
            # check if uncleaned album exists
            badFolderCheck = badFolderPath.exists()
            if badFolderCheck is True and (pathStatSize(badFolderPath) == 0):
                print("Badly named album exists and is empty.")
                sht.rmtree(badFolderPath)
                sht.move(extractFolder, albumPath)
            elif badFolderCheck is True and (pathStatSize(badFolderPath) > 0):
                print("Badly named album exists and is populated.")
                sht.move(badFolderPath, albumPath)
                sht.rmtree(extractFolder)
            elif albumCheck is False:
                print("Moving files...")
                # Move new directory in Artist directory
                sht.move(extractFolder, albumPath)
            # If album folder exists but is empty, populate it with files.
            elif albumCheck is True and (pathStatSize(albumPath) == 0):
                print("Folder exists but nothing is inside. Copying...")
                sht.copytree(extractFolder, albumPath, dirs_exist_ok=True)
                sht.rmtree(extractFolder)
            else:
                print("Album already exists here.")
                sht.rmtree(extractFolder)
            os.remove(childPath)
        fileRename(albumPath)
        print("Download Directory cleaned.")

# iterate over files to strip Artist + Album name from file name. LEAVE TRACK NUMBER


def fileRename(fileRenamePath):
    for file in fileRenamePath.iterdir():
        filePart = str(file.suffix)
        nameStrip = artistName + " - " + albumName + " - "
        newName = file.name.replace(nameStrip, "")
        newNamePath = albumPath / path.Path(newName)
        if filePart in audioExtension and pathStatSize(albumPath) > 0 and file.name == newName:
            print("Files already cleaned and existing.")
            break
        elif filePart in audioExtension and pathStatSize(albumPath) > 0:
            file.rename(newNamePath)
            # print("Renamed existing files.")
        else:
            file.rename(newNamePath)
            print("Files renamed.")


run = True

while run:

    if zipCounter(downloadPath) == 0:
        input("Press enter to exit....")
        run = False
        break
    else:
        print("******")
        allPaths = zipManager(downloadPath)
        print("******")
    print("Process completed.")
    input("Press enter to exit....")
    run = False