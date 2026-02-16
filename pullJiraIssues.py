from datetime import datetime

from atlassian import Jira


def load_jira_token(file_path: str) -> str | None:
    try:
        with open(file_path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"error: {file_path} not found.")
        return None


# 1. Configuration (using snake_case)
# Use the base URL only (no /issues/)
jira_url: str = "https://sydneydesigninc.atlassian.net"
user_email: str = "wklepacki@sydney.designinc.com.au"
# Paste your token directly here
api_token: str | None = load_jira_token(r"D:\Backup\Scripts\Jira\jira_credentials.txt")

jira = Jira(url=jira_url, username=user_email, password=api_token, cloud=True)


# Changed 'space' to 'project' as 'space' is only for Confluence
jql_query = 'project = "BIM Support Team" AND status IN ("Work in Progress", "Open") AND type != "BIM Submission Assistance"'

print(f"Searching for issues in: {jql_query}")

# 3. Fetch data
results = jira.jql(jql_query)

# 4. Access the 'issues' list
# jira.jql() returns a dictionary; the tickets are inside the 'issues' key
issues_list = results.get("issues", [])

if not issues_list:
    print("No issues found. The project name might be different in Jira's database.")
    print("Try running the 'List Projects' code below to find the exact key.")
else:
    print(f"Found {len(issues_list)} issues:\n")
    for issue in issues_list:
        ticket_key = issue["key"]
        ticket_summary = (issue["fields"].get("summary")).strip()
        ticket_status = issue["fields"].get("status", {}).get("name")
        ticket_priority = issue["fields"].get("priority", {}).get("name")
        # custom field: project name
        project_name_field_id = "customfield_10047"
        ticket_project_name = (
            issue["fields"].get(project_name_field_id)["value"]
        ).strip()
        # Pulling and formatting the created date
        ticket_created_raw = issue["fields"].get("created")
        ticket_created = (
            datetime.strptime(ticket_created_raw[:10], "%Y-%m-%d").date()
            if ticket_created_raw
            else "N/A"
        )
        # Reporter information
        ticket_reporter_data = issue["fields"].get("reporter")
        ticket_reporter = (
            ticket_reporter_data.get("displayName")
            if ticket_reporter_data
            else "Unknown"
        )

        # Pulling the due date (Jira returns YYYY-MM-DD for duedate by default)
        ticket_due_date = issue["fields"].get("duedate")
        ticket_due = ticket_due_date if ticket_due_date else "No Due Date"

        # Assignee can be None, so we handle it safely
        ticket_assignee_data = issue["fields"].get("assignee")
        ticket_assignee = (
            ticket_assignee_data.get("displayName")
            if ticket_assignee_data
            else "Unassigned"
        )

        print(
            f"{ticket_key} | {ticket_project_name} | {ticket_summary} | {ticket_status} | {ticket_priority} | {ticket_assignee} | {ticket_reporter} | {ticket_created} | {ticket_due}"
        )
