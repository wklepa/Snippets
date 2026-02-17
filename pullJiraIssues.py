import os

import pandas as pd
from atlassian import Jira


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


def LoadJiraToken(FilePath: str) -> str | None:
    try:
        with open(FilePath, "r") as F:
            return F.read().strip()
    except FileNotFoundError:
        print(f"Error: {FilePath} not found.")
        return None


def ValueDefaultStr(Value: any, Default: str = "-") -> str:
    if Value is None or str(Value).strip() == "":
        return Default
    return str(Value).strip()


def FetchJiraData(JiraInstance: Jira, JqlQuery: str, ProjectFieldId: str) -> list:
    Results: dict = JiraInstance.jql(JqlQuery)
    IssuesList: list = Results.get("issues", [])
    DataRows: list = []

    for Issue in IssuesList:
        Fields: dict = Issue.get("fields", {})

        ProjectData = Fields.get(ProjectFieldId)
        ReporterData = Fields.get("reporter")
        AssigneeData = Fields.get("assignee")

        # Safe date extraction
        RawCreated = Fields.get("created")
        TicketCreated = RawCreated[:10] if RawCreated and len(RawCreated) >= 10 else "-"

        RawDue = Fields.get("duedate")
        TicketDue = RawDue[:10] if RawDue and len(RawDue) >= 10 else "-"

        Row = {
            "Key": ValueDefaultStr(Issue.get("key")),
            "Project Name": ValueDefaultStr(
                ProjectData.get("value") if ProjectData else None
            ),
            "Summary": ValueDefaultStr(Fields.get("summary")),
            "Status": ValueDefaultStr(Fields.get("status", {}).get("name")),
            "Priority": ValueDefaultStr(Fields.get("priority", {}).get("name")),
            "Assignee": ValueDefaultStr(
                AssigneeData.get("displayName") if AssigneeData else None
            ),
            "Reporter": ValueDefaultStr(
                ReporterData.get("displayName") if ReporterData else None
            ),
            "Created": TicketCreated,
            "Due Date": TicketDue,
        }
        DataRows.append(Row)
    return DataRows


def ExportToExcelTable(
    Data: list, FileName: str, SheetName: str = "Jira_issues"
) -> None:
    # If no data is found, create a single row of placeholders
    if not Data:
        print(f"No Jira issues found. Creating placeholder report at {FileName}")
        Data = [
            {
                "Key": "-",
                "Project Name": "-",
                "Summary": "-",
                "Status": "-",
                "Priority": "-",
                "Assignee": "-",
                "Reporter": "-",
                "Created": "-",
                "Due Date": "-",
            }
        ]

    os.makedirs(os.path.dirname(FileName), exist_ok=True)
    Df = pd.DataFrame(Data)

    with pd.ExcelWriter(FileName, engine="xlsxwriter") as Writer:
        Df.to_excel(Writer, index=False, sheet_name=SheetName)
        Worksheet = Writer.sheets[SheetName]
        Worksheet.freeze_panes(1, 0)

        (MaxRow, MaxCol) = Df.shape
        ColumnNames = [{"header": col} for col in Df.columns]

        Worksheet.add_table(
            0,
            0,
            MaxRow,
            MaxCol - 1,
            {
                "columns": ColumnNames,
                "style": "TableStyleLight8",  # Apply light black & white table style
                "name": f"JiraTable_{SheetName.replace(' ', '_')}",  # Unique name per sheet
            },
        )

        for i, col in enumerate(Df.columns):
            Series = Df[col]
            MaxWidth = max(Series.astype(str).map(len).max(), len(col)) + 2
            Worksheet.set_column(i, i, min(MaxWidth, 50))

    print(f"Success: Formatted Excel table created at {FileName}")


# --- Execution ---
JiraUrl: str = "https://sydneydesigninc.atlassian.net"
UserEmail: str = "wklepacki@sydney.designinc.com.au"
TokenPath: str = r"D:\Backup\Scripts\Jira\jira_credentials.txt"
ExcelPathAllIssues: str = (
    r"N:\Temp\13. DT general\Project List Jira\Issues report\All_Issues_Jira.xlsx"
)
ExcelPathSubmisions: str = (
    r"N:\Temp\13. DT general\Project List Jira\Issues report\Submissions_Jira.xlsx"
)
ProjectFieldId: str = "customfield_10047"

ApiToken = LoadJiraToken(TokenPath)

if ApiToken:
    ScriptInfo: str = "A script to export DT Team Jira issues to the Excel files.\nA seprate files to report Work In Progress and Submissions\nissues will be created in a local folder.\nwklepacki@sydney.designinc.com.au 2024-2026"
    FormattedMessage = formatHeader(ScriptInfo)
    print(FormattedMessage)
    JiraInstance = Jira(url=JiraUrl, username=UserEmail, password=ApiToken, cloud=True)
    BimQueryAllIssue = (
        'project = "BIM Support Team" AND status IN ("Work in Progress", "Open")'
    )
    BimQuerySubmissions = (
        'project = "BIM Support Team" AND type = "BIM Submission Assistance" '
        'AND status IN ("Work in Progress", "Open")'
    )

    DataAllIssues = FetchJiraData(JiraInstance, BimQueryAllIssue, ProjectFieldId)
    DataSubmissions = FetchJiraData(JiraInstance, BimQuerySubmissions, ProjectFieldId)
    ExportToExcelTable(DataAllIssues, ExcelPathAllIssues)
    ExportToExcelTable(DataSubmissions, ExcelPathSubmisions)
