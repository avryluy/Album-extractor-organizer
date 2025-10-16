from pathlib import Path
from zipfile import ZipFile
from shutil import move, rmtree
from re import sub, compile as re_compile, match
from os import name as os_name, remove as os_remove
import logging

system_type = os_name

# VARIABLES
if system_type == "nt":
    USER_HOME = Path.home()
    SOURCE_DIRECTORY = USER_HOME / "Desktop" / "Music_Zips"
    TEMP_FILE_DIRECTORY = SOURCE_DIRECTORY / ".temp"
    DESTINATION_DIRECTORY = USER_HOME / "Music"
elif system_type == "posix":
    CURRENT_DIRECTORY = Path.cwd().parent.parent
    SOURCE_DIRECTORY = CURRENT_DIRECTORY / "Music" / "Zips"
    TEMP_FILE_DIRECTORY = SOURCE_DIRECTORY / ".temp"
    DESTINATION_DIRECTORY = CURRENT_DIRECTORY / "Music"

file_type_pattern = re_compile(
    r"^.*\.(jpg|JPG|png|PNG|flac|FLAC|mp3|MP3|wav|WAV|ogg|OGG|aiff|AIFF|txt|)$"
)

# FUNC


def sanitize_name(name: str) -> str:
    """Cleans folder and file names for filesystem safety."""
    return sub(r'[<>:"/\\|?*]', "_", name.strip())


def get_dir_size(path: Path) -> int:
    total = 0

    for file in path.rglob("*"):
        if file.is_file():
            total += file.stat().st_size
    return total


def get_zip_size(zipPath: Path) -> int:
    total = 0

    with ZipFile(zipPath, "r") as zf:
        for info in zf.infolist():
            total += info.file_size
    return total


def safe_extract(zip_path: Path, extract_to: Path) -> None:
    # check if exists in zips dir
    if not (extract_to.exists()):
        logger.info(f"Album already exists in extract path: {extract_to}")
        # print(f"Album already exists in extract path: {extract_to}")
        pass
    try:

        # open zip and extract
        with ZipFile(zip_path, "r") as zf:
            for member in zf.namelist():
                member_path = extract_to / member
                if not (
                    str(member_path.resolve()).startswith(str(extract_to.resolve()))
                ):
                    logger.exception(f"Paths not valid: {zip_path.name}: {member}")
                    raise Exception(f"Paths not valid: {zip_path.name}: {member}")

                if match(file_type_pattern, member) is None:
                    logger.exception(f"File type not supported. {member}")
                    raise Exception(f"File type not supported. {member}")

            zf.extractall(extract_to)
            logger.info(f"{zf.filename} extracted.")
            # print(f"{zf.filename} extracted.")
    except Exception as e:
        logging.exception(f"Safe extraction Failed: {e.with_traceback}")
        # print(f"Safe extraction Failed: {e.with_traceback}")


def should_skip_album(unpacked_path: Path, destination_path: Path) -> bool:
    if not destination_path.exists():
        return False

    unpacked_size = get_dir_size(unpacked_path)
    destination_size = get_dir_size(destination_path)

    difference = abs(unpacked_size - destination_size)

    if difference < 1024 * 10:
        logger.info(
            f"Skipping {destination_path.name}. Zip & Destination are the same size {unpacked_size} | {destination_size}."
        )
        # print(
        #     f"Skipping {destination_path.name}. Zip & Destination are the same size {unpacked_size} | {destination_size}."
        # )
        return True

    return False


def move_album_contents(temp_file_path: Path, library_path: Path) -> None:

    for member in temp_file_path.rglob("*"):
        name_parts = list(member.name.split(" - "))
        if len(name_parts) == 3:
            artist, album, track = name_parts
            # print(f"Aritst: {artist}, Album: {album}, Track: {track}")
        else:
            name_parts = member.parts[-2:]
            # print(f"parts: {name_parts}")
            artist, album = name_parts[0].split(" - ")
            track = name_parts[1]

        artist_folder = library_path / sanitize_name(artist)
        album_folder = artist_folder / sanitize_name(album)
        track_path = album_folder / sanitize_name(track)

        if not artist_folder.exists():
            artist_folder.mkdir(exist_ok=True)

        if not album_folder.exists():
            album_folder.mkdir(exist_ok=True)

        if member.is_file() and track_path.exists():
            logger.info(f"File {member.name} exists.\nSkipping...\n")
            # print(f"File {member.name} exists.\nSkipping...\n")
        logger.info(f"Moving file {member.name}\n...From {member}\n...To {track_path}")
        # print(f"Moving file {member.name}\n...From {member}\n...To {track_path}")
        move(member, track_path)
    return


def cleanup_dir(path: Path) -> None:

    for files in path.rglob("*"):
        try:
            if files.is_file():
                logger.info(f"Deleting file: {files}")
                # print(f"Deleting file: {files}")
                os_remove(files)
            elif files.is_dir():
                logger.info(f"Deleting directory: {files}")
                # print(f"Deleting directory: {files}")
                rmtree(files)
        except Exception as e:
            logger.exception(f"Error deleting file tree: {e.with_traceback}")
            # print(f"Error deleting file tree: {e.with_traceback}")
            continue
    return


# PROGRAM
def main() -> int:
    if not (SOURCE_DIRECTORY.exists()):
        SOURCE_DIRECTORY.mkdir()
    if not (TEMP_FILE_DIRECTORY.exists()):
        TEMP_FILE_DIRECTORY.mkdir()

    zip_files = list(SOURCE_DIRECTORY.glob("*.zip"))

    if not zip_files:
        cleanup_dir(SOURCE_DIRECTORY)
        logger.info("No zips to unpack. Exiting\n")
        # print("No zips to unpack. Exiting\n")
        return 0

    for zip_path in zip_files:
        unpack_folder = TEMP_FILE_DIRECTORY / zip_path.stem
        if unpack_folder.exists():
            logger.info(f"Unpacked album already exists: {unpack_folder}")
            # print(f"Unpacked album already exists: {unpack_folder}")
        else:
            try:
                logger.info(f"Creating dir at: {unpack_folder}")
                # print(f"Creating dir at: {unpack_folder}")
                unpack_folder.mkdir(exist_ok=True)
                safe_extract(zip_path, unpack_folder)

            except Exception as e:
                logger.exception(f"Error extracting album: {e.with_traceback}")
                # print(f"Error extracting album: {e.with_traceback}")
                return 1
        artist, album = zip_path.stem.split(" - ")
        album_destination = DESTINATION_DIRECTORY / artist / album

        if should_skip_album(zip_path, album_destination) is True:
            logger.info(
                f"Album being skipped due to already being in library: {album_destination}"
            )
            # print(
            #     f"Album being skipped due to already being in library: {album_destination}"
            # )
        else:
            logger.info(f"Album does NOT exist in library: {album_destination}")
            # print(f"Album does NOT exist in library: {album_destination}")

        try:
            move_album_contents(unpack_folder, DESTINATION_DIRECTORY)
            logger.info(f"{album} moved successfully.")
            # print(f"{album} moved successfully.")
        except Exception as e:
            logger.exception(f"Error moving {album}: {e.with_traceback}")
            # print(f"Error moving {album}: {e.with_traceback}")
            return 1

    cleanup_dir(SOURCE_DIRECTORY)
    logger.info("Directory Cleaned.")
    # print("Directory Cleaned.")
    return 0


if __name__ == "__main__":
    # LOGS
    filepath = Path.cwd() / "logs" / "albumextractor.log"
    logger = logging.getLogger(__name__)

    logging.basicConfig(
        filename=filepath,
        format="%(asctime)s, %(levelname)s, " "%(funcName)s, %(lineno)d, %(message)s",
        encoding="utf-8",
        level=logging.DEBUG,
    )
    main()
    logging.shutdown()
