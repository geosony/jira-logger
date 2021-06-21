import os
import configparser as configparser

config_file = os.environ.get("JIRA_CONFIG_FILE")
config = configparser.ConfigParser()
config.read(config_file)

apitoken = config['jira']['api_token']
api = config['jira']['url']
user = config['jira']['user']

comment_file = config['jira']['comment_file']  

auth = (user, apitoken)
headers = {
    "Accept": "application/json",
    "content-type":"application/json"
}

