import argparse
import datetime

x = datetime.datetime.now()
today_str = x.strftime("%Y-%m-%d")

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=False)
group.add_argument("-i", "--interactive", action="store_true",  help="Interactive Mode")
group.add_argument("-o", "--oneline", action="store",  help="give a oneline string like '<Jira-ID>|<spent_time>|<start-time>|<date>|<comment>' Jira ID should be the first value and comment the last value; Jira ID is mandatory; comment can be read from file with -f option")
group.add_argument("-s", "--splitmode", action="store_false",  help="Split-wise arguments; will be default; if not using -i or -o option")
parser.add_argument("-t", "--start-time", action="store", help="Exact time when the work started; if not given the time will be calculated from time_spent attr")
parser.add_argument("-x", "--time-spent", action="store", default="1d", help="Time spent; '8h', '1h30m', '45m'")
parser.add_argument("-j", "--jira-id", action="store", help="Jira ID")
parser.add_argument("-d", "--log-date", action="store", default="{}".format(today_str), help="Date of work/task; YYYY-MM-DD format; Default date is today")
parser.add_argument("-m", "--comment", action="store", help="Comment your work")
parser.add_argument("-f", "--file_comments", action="store_true",  help="Read comment from file; add your comments to log.txt")

args = parser.parse_args()
