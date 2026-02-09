import sys

try:
    import os
except ImportError as e:
    print(f"Error importing module: {e}")
    sys.exit(1)

"""
Define default values for CSV folder, projects folder, output file, output extension, and CSV header and script info.
"""
defualtCsvFolder: str = r"N:\Temp\13. DT general\Project List Jira"
defaultProjectsFolder: str = r"X:\2. Projects"
defaultOutputFile: str = "DesignInc_ProjectList v"
defaulOutputExtension: str = ".csv"
csvHeader: str = "Id,ProjectNumber,Projectname,Assignee,IsActive,NameNumber"

scriptInfo: str = f"A script to list all the projects in {defaultProjectsFolder} folder\nProjects are exported to {defualtCsvFolder}\nfolder, and placed in the latest CSV (vXX).\nwklepacki@sydney.designinc.com.au 2024-2026"
"""
Function to format a header. It centers the lines and infills spaces with border
symbols and whitespaces.
"""


def formatHeader(
    header: str, symbolNum: int = 3, spaceNum: int = 3, symbolTyp: str = "*"
) -> str:
    # Clean and split lines
    lines = [line.strip() for line in header.split("\n")]
    if not any(lines):
        return ""

    # Calculate dimensions
    max_line_len = max(len(line) for line in lines)
    # Total width of the entire header block
    total_width = max_line_len + 2 * (symbolNum + spaceNum)
    # The width available for text + internal padding
    content_width = total_width - (2 * symbolNum)

    # Build the components
    border_line = symbolTyp * total_width
    side_border = symbolTyp * symbolNum

    tempHeader = [border_line]

    for line in lines:
        # The '^' centers the text within 'content_width'
        # f-string syntax: {value:^[width]}
        centered_text = f"{line:^{content_width}}"
        tempHeader.append(f"{side_border}{centered_text}{side_border}")

    tempHeader.append(border_line)
    # Return formatted output
    return "\n".join(tempHeader) + "\n"


"""
Function to find the latest version number in a folder
@param csvFolder: The folder path to search for CSV files
@return: The latest version number found, or None if no versions are found
"""


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


"""
Function to list all projects in a folder
@param projectsFolder: The folder path to search for projects
@return: A list of project numbers and names
"""


def projectList(projectsFolder: str):
    projectNumberName: list[
        str
    ] = []  # Initialize an empty list to store project number and name
    projectNumberName.append(csvHeader)  # Append the header row to the list
    defaultAssignee: str = "wklepacki@sydney.designinc.com.au"

    # Check if the projects folder exists and list its contents
    if os.path.isdir(projectsFolder):
        projectsMain: list[str] = [
            x for x in os.listdir(projectsFolder) if x.isnumeric()
        ]

        # Iterate through the main projects
        for project in projectsMain:
            # Check if the project is a directory and list its contents
            if os.path.isdir(os.path.join(projectsFolder, project)):
                subProjects: list[str] = [
                    x
                    for x in os.listdir(os.path.join(projectsFolder, project))
                    if x.startswith("P")
                ]

                # Iterate through the subprojects
                for subProject in subProjects:
                    getNumber: str = subProject[
                        :7
                    ]  # Extract the number part of the subproject name
                    getName: str = subProject[7:].lstrip(
                        "-_ "
                    )  # Extract the name part of the subproject name
                    wrapName: str = (
                        '"' + getName + '"'
                    )  # Wrap the name in double quotes
                    wrapNumberName: str = '"' + getNumber + " " + getName + '"'
                    numberName: str = f"{getNumber},{getNumber},{wrapName},{defaultAssignee},TRUE,{wrapNumberName}"  # Format the number and name as a string
                    # Append the formatted string to the projectNumberName list
                    projectNumberName.append(numberName)

    # Return the projectNumberName list if it's not empty, otherwise return None
    return projectNumberName if projectNumberName else None


"""
Function to write a CSV file with project information
@param projectNumberName: List of project numbers and names
@param outputFolder: Folder path to save the CSV file
@param outputName: Name of the CSV file
@param outputExtension: Extension of the CSV file
@param version: Version number of the CSV file
@return: Name of the CSV file
"""


def writeFile(
    projectNumberName: list[str],
    outputFolder: str,
    outputName: str,
    outputExtension: str,
    version: int,
) -> str:
    # Create version
    versionString: str = str(version + 1)
    # Create file name
    fileName: str = f"{outputName}{versionString}{outputExtension}"
    # Create the output file path
    outputFilePath: str = os.path.join(outputFolder, fileName)

    # Open the output file in write mode
    with open(outputFilePath, "w") as file:
        for line in projectNumberName:
            file.write(line + "\n")
    return fileName


# Make the script work
listOfProjects: list[str] | None = projectList(
    defaultProjectsFolder
)  # Call projectList function
currentVersion: int | None = findVersion(defualtCsvFolder)  # Call findVersion function

# Call the writeFile function if listOfProjects and currentVersion are not None
if listOfProjects and currentVersion:
    # Print the script info
    formatInfo: str = formatHeader(scriptInfo)
    print(formatInfo)
    try:
        outputName: str = writeFile(
            listOfProjects,
            defualtCsvFolder,
            defaultOutputFile,
            defaulOutputExtension,
            currentVersion,
        )
        print(f"\nDirectory: {defualtCsvFolder}")
        print(f"File {outputName} created successfully!")
        print(f"Projects Synced: {len(listOfProjects) - 1}")
    except Exception as e:
        print(f"\nCRITICAL ERROR: Could not write file:\n{e}")
