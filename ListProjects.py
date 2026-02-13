import sys

"""
Ensure that the required modules are installed.
"""
try:
    import os
except ImportError as e:
    print(f"Error importing module: {e}")
    sys.exit(1)

"""
 --- CONFIGURATION ---
"""
defaultCsvFolder: str = r"N:\Temp\13. DT general\Project List Jira"
defaultProjectsFolder: str = r"X:\2. Projects"
defaultOutputFile: str = "DesignInc_ProjectList v"
defaultOutputExtension: str = ".csv"
csvHeader: str = "Id,ProjectNumber,Projectname,Assignee,IsActive,NameNumber"

# Generate office-wide projects
officeWide: dict[str, str] = {
    "PXX-XX1": "Project Start-up",
    "PXX-XX2": "Officewide Implementation",
    "PXX-XX3": "General Request",
}
# Default project assignee
defaultAssignee: str = "wklepacki@sydney.designinc.com.au"
# Script information
scriptInfo: str = f"A script to list all the projects in {defaultProjectsFolder} folder\nProjects are exported to {defaultCsvFolder}\nfolder, and placed in the latest CSV (vXX).\nwklepacki@sydney.designinc.com.au 2024-2026"


def ProjectsOfficeWide(projectOfficeWide: dict[str, str], assignee: str) -> list[str]:
    """
    Generates a list of office-wide projects formatted for the CSV file.

    Args:
        projectOfficeWide (dict[str, str]): Dictionary mapping project numbers to names.
        assignee (str): Email address of the project assignee.

    Returns:
        list[str]: A list of formatted project data strings.
    """
    officeProjects = []  # Initialize an empty list to store the formatted project data
    for getNumber, getName in projectOfficeWide.items():
        wrapName: str = '"' + getName + '"'  # Wrap the name in double quotes
        wrapNumberName: str = (
            '"' + getNumber + " " + getName + '"'
        )  # Wrap the number and name in double quotes
        numberName: str = f"{getNumber},{getNumber},{wrapName},{assignee},TRUE,{wrapNumberName}"  # Format the number and name as a string
        officeProjects.append(
            numberName
        )  # Append the formatted project data to the list
    return officeProjects


def formatHeader(
    header: str, symbolNum: int = 3, spaceNum: int = 3, symbolTyp: str = "*"
) -> str:
    """
    Formats a header by centering the lines and infilling spaces with border symbols.

    Args:
        header (str): Header text to be formatted.
        symbolNum (int): Number of symbols on each side of the header.
        spaceNum (int): Number of spaces between the header and the border.
        symbolTyp (str): Symbol type to use for the border.

    Returns:
        str: The formatted header string.
    """
    # Clean and split lines return "" if lines is empty
    lines: list[str] = [line.strip() for line in header.split("\n")]
    if not lines:
        return ""

    # Calculate dimensions
    max_line_len: int = max(len(line) for line in lines)
    # Total width of the entire header block
    total_width: int = max_line_len + 2 * (symbolNum + spaceNum)
    # The width available for text + internal padding
    content_width: int = total_width - (2 * symbolNum)

    # Build the components
    border_line: str = symbolTyp * total_width
    side_border: str = symbolTyp * symbolNum

    tempHeader: list[str] = [border_line]

    for line in lines:
        # The '^' centers the text within 'content_width'
        # f-string syntax: {value:^[width]}
        centered_text: str = f"{line:^{content_width}}"
        tempHeader.append(f"{side_border}{centered_text}{side_border}")

    tempHeader.append(border_line)
    # Return formatted output
    return "\n".join(tempHeader) + "\n"


def findVersion(csvFolder: str) -> int | None:
    """
    Finds the latest version number in a folder by checking file names.
    Assumes files are named with a 'v' followed by the version number (e.g., '...v12.csv').

    Args:
        csvFolder (str): The folder path to search for CSV files.

    Returns:
        int | None: The latest version number found, or None if no versions are found.
    """
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


def projectList(projectsFolder: str, assignee: str) -> list[str] | None:
    """
    Lists all projects in the specified folder and adds office-wide defaults.

    Args:
        projectsFolder (str): The folder path to search for projects.
        assignee (str): Email address of the project assignee.

    Returns:
        list[str] | None: A list of formatted project strings including the header.
    """
    projectNumberName: list[
        str
    ] = []  # Initialize an empty list to store project number and name
    projectNumberName.append(csvHeader)  # Append the header row to the list

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
                    numberName: str = f"{getNumber},{getNumber},{wrapName},{assignee},TRUE,{wrapNumberName}"  # Format the number and name as a string
                    # Append the formatted string to the projectNumberName list
                    projectNumberName.append(numberName)

    # Return the projectNumberName list if it's not empty, otherwise return None
    officeWideXXX: list[str] = ProjectsOfficeWide(officeWide, defaultAssignee)
    return projectNumberName + officeWideXXX if projectNumberName else None


def writeFile(
    projectNumberName: list[str],
    outputFolder: str,
    outputName: str,
    outputExtension: str,
    version: int,
) -> str:
    """
    Writes the project list to a CSV file with an incremented version number.

    Args:
        projectNumberName (list[str]): List of project numbers and names.
        outputFolder (str): Folder path to save the CSV file.
        outputName (str): Base name of the CSV file.
        outputExtension (str): Extension of the CSV file.
        version (int): Current version number.

    Returns:
        str: Name of the created CSV file.
    """
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


"""
 --- EXECUTION ---
"""
listOfProjects: list[str] | None = projectList(
    defaultProjectsFolder, defaultAssignee
)  # Call projectList function
currentVersion: int | None = findVersion(defaultCsvFolder)  # Call findVersion function

# Call the writeFile function if listOfProjects and currentVersion are not None
if listOfProjects and currentVersion:
    # Print the script info
    formatInfo: str = formatHeader(scriptInfo)
    print(formatInfo)
    try:
        outputName: str = writeFile(
            listOfProjects,
            defaultCsvFolder,
            defaultOutputFile,
            defaultOutputExtension,
            currentVersion,
        )
        # Print statistics
        print(f"\nDirectory: {defaultCsvFolder}")
        print(f"File {outputName} created successfully!")
        print(
            f"Projects Synced: {len(listOfProjects) - 1}\nThe sample output listed below:"
        )
        # Output the first 10 projects
        for index, project in enumerate(listOfProjects):
            if index < 10:
                print(f"Project {index + 1}: {project}")
    except Exception as e:
        print(f"\nCRITICAL ERROR: Could not write file:\n{e}")
