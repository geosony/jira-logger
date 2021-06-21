"""
Log work in Jira
"""
import json
import requests
import datetime
import re

from jira_logger.config import api, auth, headers, comment_file
from jira_logger.options import args, today_str

class JiraToolKit:


    def __init__(self):
        self.values = self.set_values()

    def get_logs_from_file(self, logs_file):
        logs = []
        newline = {"type": "hardBreak"}
        with open(logs_file) as flogs:
            for line in flogs:
                logs.append({"text": line, "type": "text"})
                logs.append(newline)
        return logs[:-1]
    
    
    def log_work(self, task, log):
        url = f"{api}/issue/{task}/worklog"
        response = requests.request(
           "POST",
           url,
           data=log,
           headers=headers,
           auth=auth
        )
    
        print(json.dumps(
                json.loads(response.text), 
                sort_keys=True, 
                indent=4, 
                separators=(",", ": ")))
    
    def calc_time(self, ts):
    
        m = re.match(r'(?:(\d+)h\s*)?(?:(\d+)m)?', ts)
    
        if m:
            th = int(m.group(1)) if m.group(1) else 0
            tm = int(m.group(2)) if m.group(2) else 0
        else:
            return False
    
        d = datetime.datetime.today() - datetime.timedelta(hours=th, minutes=tm)
        return d.strftime('%H:%M')
    
    def set_values(self):
    
        comment_from_file = False
        log_date = today_str
        start_time = ''
    
        if args.file_comments:
            comment_from_file = True
    
        if args.interactive:
            mode="interactive"
            try:
                time_spent = input("Spent hours: ")
                start_time = input("Start time: ")
                log_date = input("Work date: ") 
                jira_id = input("Jira ID: ")
                if not comment_from_file:
                    comment = input("Comment: ")
            except KeyboardInterrupt:
                print("\n\nBye, prepare your log and try next time; \nFor the command help try --help or \h option.!!\n")
                exit()
    
        elif args.oneline:
            mode="oneline"
            oneline_str = args.oneline
            val_arr = oneline_str.split('|')
    
            comment = None
            if not comment_from_file:
                comment = val_arr[-1]
            
            try:
                jira_id = val_arr[0]
                m = re.search(r'\|((?:\d+h\s*)?(?:\d+m)?)\|?', oneline_str)
                if m:
                    time_spent = m.group(1)
                else:
                    print("Time spent is mandatory")
                    exit()

                m1 = re.search(r'\|(\d+:\d+)\|?', oneline_str)
                if m1:
                    start_time = m1.group(1)
    
                m2 = re.search(r'\|(\d{4}(?:-\d{2}){2})\|?', oneline_str)
                if m2:
                    log_date = m2.group(1)
    
            except IndexError:
                print("Jira ID and Time spent are mandatory")
                exit()
            
        elif args.splitmode:
            mode="split"
            time_spent = args.time_spent
            start_time = args.start_time
            log_date = args.log_date
            comment = args.comment
            if args.jira_id is None:
                print("Jira ID should not be blank; use -j 'Jira-ID'")
                exit()
            else:
                jira_id = args.jira_id
    
        start_time = start_time if start_time else self.calc_time(time_spent)
    
        if comment_from_file:
            log = self.get_logs_from_file(comment_file)
        else:
            if not comment:
                print("Comment should not be blank!")
                exit()
            log = [{"text": comment, "type": "text"}]

        try:
            if not re.match(r"[a-zA-Z]{1,5}-[0-9]{1,5}", jira_id):
                print("Invalid Jira ID")
                exit()
        except IndexError:
            print("Jira ID is mandatory!!")
            exit()

        if not start_time:
            print("Invalid time or start time!!")
            exit()
        
        self.jiraID = jira_id
        
        values = {
                "time_spent": time_spent,
                "start_time": start_time,
                "log_date": log_date,
                "jira_id": jira_id,
                "work_log": log,
                }

        return values
    
    def create_jira_log(self): 
        return json.dumps({
          "timeSpent": self.values["time_spent"],
          "comment": {
            "type": "doc",
            "version": 1,
            "content": [
              {
                "type": "paragraph",
                "content": self.values["work_log"]
              }
            ]
          },
          "started": "{}T{}:00.000+0530".format(self.values["log_date"], self.values["start_time"])
        })


log_handle = JiraToolKit()
