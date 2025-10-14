import os
import shutil
import re
import zipfile
from pathlib import Path

audioExtension = (".wav", ".mp3", ".aac", ".flac", ".ogg", ".alac", ".aiff")
SOURCE_DIR = Path.home() / "Desktop" / "Music_Zips"
DEST_DIR = Path.home() / "Music"
TEMP_EXTRACT_DIR = SOURCE_DIR / "zzExtracted"


def safe_extract(zip_path: Path, extract_to: Path) -> None:

    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.namelist():
            member_path = extract_to / member
            if not str(member_path.resolve()).startswith(str(extract_to.resolve())):
                raise Exception(f"Bad File path: {zip_path.name}: {member}")

            zf.extractall(extract_to)
        print("Extracted")


def sanitize_name(name: str) -> str:
    """Cleans folder and file names for filesystem safety."""
    return re.sub(r'[<>:"/\\|?*]', "_", name.strip())


def get_zip_uncompressed_size(zip_path: Path) -> int:
    """Returns total uncompressed size of all files in a ZIP archive."""
    total = 0
    with zipfile.ZipFile(zip_path, "r") as zf:
        for info in zf.infolist():
            total += info.file_size
    return total


def get_directory_size(path: Path) -> int:
    """Returns total size of all files in a directory (recursively)."""
    total = 0
    for file in path.rglob("*"):
        if file.is_file():
            total += file.stat().st_size
    return total


def should_skip_album(zipPath: Path, destinationPath: Path) -> bool:
    size_check = get_directory_size(destinationPath) == get_zip_uncompressed_size(
        zipPath
    )

    if destinationPath.exists() & size_check is True:
        # print("Album exists in Library & is same size as zip contents")
        return True
    return False


# Scan source_destination for .zip files.
zip_files = list(Path(SOURCE_DIR).glob("*.zip"))


if not zip_files:
    print("No zips found. Exiting\n")  # For each .zip:

for zip_path in zip_files:
    # Get clean folder name
    artist_name, album_name = zip_path.stem.split(" - ")
    # Determine an unpack folder name (e.g. same as the zip filename).

    unpacked_folder = TEMP_EXTRACT_DIR / zip_path.stem
    destination_folder = DEST_DIR / artist_name / album_name
    # If unpack folder exists → skip extraction.
    if should_skip_album(zip_path, destination_folder) is True:
        print(f"Album {album_name} exists in library: {destination_folder}")
    # Else → extract into a temp/unpack folder.
    else:
        print(f"{zip_path.stem} does not exist")
        safe_extract(zip_path, unpacked_folder)


# For each unpacked album folder:

# Parse artist and album name (from folder or metadata if available).

# Construct target path:
# final_destination / artist / album_name

# Create missing directories.

# Check for duplicates before moving (maybe compare filenames).

# Move or copy all track files.

# If all files successfully moved → delete unpacked folder.

# Optional: log skipped/moved albums for later review.
