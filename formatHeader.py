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


"""
--- TEST FUNCTION ---
"""
defaultProjectsFolder: str = "XXXX"
defaultCsvFolder: str = "YYYY"
scriptInfo: str = f"A script to list all the projects in {defaultProjectsFolder} folder\nProjects are exported to {defaultCsvFolder}\nfolder, and placed in the latest CSV (vXX).\nwklepacki@sydney.designinc.com.au 2024-2026"
formattedMessage = formatHeader(scriptInfo)
print(formattedMessage)
