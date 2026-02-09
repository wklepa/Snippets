import os

csvFolder = r"N:\Temp\13. DT general\Project List Jira"


def findVersion(csvFolder: str) -> int | None:
    extension: str = ".csv"  # Extension for CSV files
    versions: list[int] = []  # List to store versions
    for item in os.listdir(csvFolder):
        nameExtension = os.path.splitext(item)
        if nameExtension[-1].lower() == extension:
            fileName = nameExtension[0]
            try:
                getVIndex: int = fileName.rindex("v")
                getNumber: str = fileName[(getVIndex + 1) :].strip()
                if getNumber.isnumeric():
                    versions.append(int(getNumber))
            except ValueError:
                pass

    return max(versions) if versions else None  # Return None if no versions found


maxVersion = findVersion(csvFolder)
print(maxVersion)
