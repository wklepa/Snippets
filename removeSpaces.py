# imports
import sys

try:
    import os
    # import other modules
except ImportError:
    sys.exit("Script failed to import critical modules!")

"""
Procedure to remove whitespaces from a file
It removes leading, trailing, or both leading and trailing whitespaces from a file.
"""

# user inputs file
exitFlagF: bool = True
dirFileName: str = ""  # Initialize dirFileName variable before using it
while exitFlagF:
    dirFileName = (input("Enter file name and location:\n")).strip()
    if os.path.isfile(dirFileName) or dirFileName == "":
        exitFlagF = False

# Process files and remove whitespaces
if dirFileName != "":
    # user inputs strip option
    inclusion: dict = {"l": "leading", "r": "trailing", "b": "leading and trailing"}
    exitFlagO: bool = True
    stripOption: str = ""  # Initialize stripOption variable before using it
    while exitFlagO:
        stripOption = (input("Enter strip option (l/r/b):\n")).strip().lower()
        if stripOption in inclusion:
            exitFlagO = False
    # read file content
    with open(dirFileName, "r") as fr:
        currentLines: list[str] = fr.readlines()
    # remove leading whitespaces
    amendedLines: list[str] = []
    for line in currentLines:
        if stripOption == "l":
            amendedLines.append(line.lstrip())
        elif stripOption == "r":
            # rstrip() removes the \n, so I add it back
            amendedLines.append(line.rstrip() + "\n")
        elif stripOption == "b":
            # strip() removes both ends, including the \n
            amendedLines.append(line.strip() + "\n")
    # write file content
    if amendedLines:
        with open(dirFileName, "w") as fw:
            fw.writelines(amendedLines)
        print(f"The {inclusion[stripOption]} whitespaces were removed.")
    else:
        print("The file is empty.")
else:
    print("No changes were done...\n")
