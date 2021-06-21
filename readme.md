## Log your work in Jira: Command-line

If you are a hard core command-line user, and if you want to log your work in Jira daily, this repo will help you.

### Setup

#### Steps

- Copy config.local.ini to your favorite location (can be the same folder) and rename it to config.ini set values to all keys.

```
[jira]

api_token = xxxxxxxxxxxxxxxxxxxxxxx # Obtain a token from https://id.atlassian.com/manage/api-tokens
url = https://xxxxxxxxxxxx.atlassian.net/rest/api/3 # change xxxx with your subdomain (would be your organisation name)
user = foo@example.com # Jira user name

comment_file = /path/to/log.txt # here you can add your comment/log description; if you chose to load comments from file.

```

- create shortcut for the command; add the following line to .zshrc or .bashrc; *there are also many alternative ways to do this*

```

export JIRA_CONFIG_FILE=/path/to/the/config.ini
alias log_jira="`which python3` /path/to/this/repo"

```

- run command `log_jira -h` for help


### Usage

- `log_jira -i` for the interactive mode
- `log_jira -j "<JIRA_TICKET_ID>" -x 2h -t 09:30 -m"My work description"` for the split options mode; -j is mandatory.
- `log_jira -o "<JIRA_TICKET_ID>|1h30m|14:30|2021-04-22|My work summary" for one line comment mode
- ` -f` option will override the comment option in all modes and will be taken from the text in `log.txt`; Multi-line comments;
- Enter 'y', 'yes', 'ok', .. to submit log to jira after confirming your request.


```
> log_jira -h
usage: jira [-h] [-i | -o ONELINE | -s] [-t START_TIME] [-x TIME_SPENT] [-j JIRA_ID] [-d LOG_DATE] [-m COMMENT] [-f]

optional arguments:
  -h, --help            show this help message and exit
  -i, --interactive     Interactive Mode
  -o ONELINE, --oneline ONELINE
                        give a oneline string like '<Jira-ID>|<spent_time>|<start-time>|<date>|<comment>' Jira ID should be the first value and comment the last value; Jira ID is mandatory; comment can be read
                        from file with -f option
  -s, --splitmode       Split-wise arguments; will be default; if not using -i or -o option
  -t START_TIME, --start-time START_TIME
                        Exact time when the work started; if not given the time will be calculated from time_spent attr
  -x TIME_SPENT, --time-spent TIME_SPENT
                        Time spent; '8h', '1h30m', '45m'
  -j JIRA_ID, --jira-id JIRA_ID
                        Jira ID
  -d LOG_DATE, --log-date LOG_DATE
                        Date of work/task; YYYY-MM-DD format; Default date is today
  -m COMMENT, --comment COMMENT
                        Comment your work
  -f, --file_comments   Read comment from file; add your comments to log.txt
```
