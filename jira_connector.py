from jira import JIRA
import os

JIRA_BASE_URL = os.getenv("jira-base-url")
JIRA_API_KEY = os.getenv("jira-api-key")
JIRA_USER = os.getenv("jira-user")
jira = JIRA(server=JIRA_BASE_URL, basic_auth=(JIRA_USER, JIRA_API_KEY))