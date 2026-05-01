# imports
import sys

try:
    import os
    # import other modules
except ImportError:
    sys.exit("Script failed to import critical moduls!")

"""
listDir(sourcePath: str) -> str | bool

Lists the contents of a directory and prompts the user to select a file.
Args:
    sourcePath (str): The path to the directory to list.

Returns:
    str | bool: The selected file path or False if no file is selected.
"""


def listDir(sourcePath: str) -> str | bool:
    if not os.path.isdir(sourcePath):
        return False

    listFiles: list[str] = os.listdir(sourcePath)
    if not listFiles:
        return False

    # Print the list with aligned indices
    padding: int = len(str(len(listFiles)))
    for i, e in enumerate(listFiles, 1):
        print(f"{str(i).zfill(padding)}: {e}")

    while True:
        userIndex: str = input(
            f"Enter file index in range 1-{len(listFiles)} (or 'q' to quit): "
        ).strip()

        if userIndex.lower() == "q":
            return False

        if userIndex.isdigit():
            idx: int = int(userIndex)
            if 1 <= idx <= len(listFiles):
                # Subtract 1 because list index starts at 0
                fileConsider: str = listFiles[idx - 1]
                print(f'Considering the "{fileConsider}" file...')
                return os.path.join(sourcePath, fileConsider)

        print("Invalid selection. Try again.")


# Test run using sample directory path
listDir(r"/home/voy/Downloads")
