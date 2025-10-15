from pathlib import Path
import zipfile
import shutil as sht
import re
import os as os


# VARIABLES
USER_HOME = Path.home()
SOURCE_DIRECTORY = USER_HOME / "Desktop" / "Music_Zips"
TEMP_FILE_DIRECTORY = SOURCE_DIRECTORY / ".temp"


# FUNC


def sanitize_name(name: str) -> str:
    """Cleans folder and file names for filesystem safety."""
    return re.sub(r'[<>:"/\\|?*]', "_", name.strip())


def get_dir_size(path: Path) -> int:
    total = 0
    for file in path.rglob("*"):
        if file.is_file():
            total += file.stat().st_size
    return total


def get_zip_size(zipPath: Path) -> int:
    total = 0

    with zipfile.ZipFile(zipPath) as zf:
        for info in zf.infolist():
            total += info.file_size
    return total


def safe_extract(zip_path: Path, extract_to: Path) -> None:
    # check if exists in zips dir
    zip_dir_size = get_zip_size(zip_path)

    extract_dir_size = get_dir_size(extract_to)

    if not (zip_dir_size == extract_dir_size):
        print(f"Album already exists in extract path: {extract_to}")
    try:

        # open zip and extract
        with zipfile.ZipFile(zip_path, "r") as zf:
            for member in zf.namelist():
                member_path = extract_to / member
                if not (
                    str(member_path.resolve()).startswith(str(extract_to.resolve()))
                ):
                    raise Exception(f"Paths not valid: {zip_path.name}: {member}")
                print(f"Paths valid: {zip_path.name}: {member}")
            zf.extractall(extract_to)
    except Exception as e:
        print(f"Safe extraction Failed: {e.with_traceback}")


def move_album_contents():
    return


def cleanup_temp_files():
    return


# PROGRAM
def main() -> int:

    if not (SOURCE_DIRECTORY.exists()):
        SOURCE_DIRECTORY.mkdir()
    if not (TEMP_FILE_DIRECTORY.exists()):
        TEMP_FILE_DIRECTORY.mkdir()

    zip_files = list(SOURCE_DIRECTORY.glob("*.zip"))

    if not zip_files:
        print("No zips to unpack. Exiting\n")

    for files in zip_files:
        unpack_folder = files.stem
        print(unpack_folder)

    return 0


if __name__ == "__main__":
    main()
