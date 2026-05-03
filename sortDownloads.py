import sys
import threading
import time

try:
    import os
    import shutil
except ImportError:
    sys.exit("Script failed to import critical modules!")

# Constants
CATEGORIES = [
    {"folder": "PDF", "types": [".pdf"]},
    {
        "folder": "DOC",
        "types": [".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt"],
    },
    {"folder": "IMG", "types": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"]},
    {"folder": "ARC", "types": [".zip", ".rar", ".7z", ".tar", ".gz"]},
    {"folder": "APP", "types": [".deb", ".rpm", ".sh", ".appimage"]},
]

downloads_folder = r"/home/voy/Downloads"
counter = 0


def spin(stop_event):
    progress_chars = ["-", "/", "|", "\\"]
    while not stop_event.is_set():
        for char in progress_chars:
            if stop_event.is_set():
                break
            # \r moves cursor to start, end="" prevents newline
            print(f"\rSorting... {char}", end="", flush=True)
            time.sleep(0.1)
    # Clear the spinner line when done
    print("\r" + " " * 20 + "\r", end="", flush=True)


def main():
    global counter
    print("Organizing the Downloads folder...")

    if not os.path.exists(downloads_folder):
        print(f"Error: The folder {downloads_folder} does not exist.")
        return

    # --- Start Spinner ---
    stop_spinner = threading.Event()
    spinner_thread = threading.Thread(target=spin, args=(stop_spinner,))
    spinner_thread.start()

    try:
        for file in os.listdir(downloads_folder):
            file_path = os.path.join(downloads_folder, file)
            if not os.path.isfile(file_path):
                continue

            file_ext = os.path.splitext(file)[1].lower()
            moved = False

            # Check known categories
            for category in CATEGORIES:
                if file_ext in category["types"]:
                    dest_folder = os.path.join(downloads_folder, category["folder"])
                    os.makedirs(dest_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(dest_folder, file))
                    counter += 1
                    moved = True
                    break

            # If it didn't match any category, move to OTH
            if not moved:
                dest_folder = os.path.join(downloads_folder, "OTH")
                os.makedirs(dest_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(dest_folder, file))
                counter += 1

    finally:
        # --- Stop Spinner ---
        stop_spinner.set()
        spinner_thread.join()

    if counter == 0:
        print("No files moved.")
    else:
        print(f"Success! Sorted {counter} files.")


if __name__ == "__main__":
    main()
