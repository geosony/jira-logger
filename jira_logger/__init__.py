from jira_logger.jira_toolkit import log_handle


def main():

    log = log_handle.create_jira_log()

    print(log)
    
    jiraID = log_handle.jiraID
    
    try:
        confirm = input("Submit log ({}): ".format(jiraID))
    except KeyboardInterrupt:
        print("\n\nBye, prepare your log and try next time; \nFor the command help try --help or \h option.!!\n")
        exit()
    
    yes_set = {'y', 'yes', 'Yes', 'Y', 'ok', 'OK', 'Ok'}
    
    if confirm in yes_set:
        print("Submitting your log to Jira..")
        log_handle.log_work(jiraID, log)

main()
