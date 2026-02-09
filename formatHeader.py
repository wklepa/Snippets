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


# Test function
message: str = "jehevow dkjfnkfef\nfvmvoemvomv ofw\nerfeffre"
defaultProjectsFolder: str = "XXXX"
defualtCsvFolder: str = "YYYY"
scriptInfo: str = f"A script to list all the projects in {defaultProjectsFolder} folder\nProjects are exported to {defualtCsvFolder}\nfolder, and placed in the latest CSV (vXX).\nwklepacki@sydney.designinc.com.au 2024-2026"
formattedMessage = formatHeader(scriptInfo)
print(formattedMessage)
