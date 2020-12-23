# toggler

Toggler will toggle time entry to toggl track from your akashi timestamp log.

## Requirements

- Python 3.9+
- pip
  - requests
- [fzf](https://github.com/junegunn/fzf) (Optional.)

## toggler.py

The main system. Execute this code to toggle.

Also, your command log will be collected to the logs folder, but don't care about it. It's in the .gitignore file.

### Arguments

All arguments are required.

```
usage: toggler.py [-h] [-t TOGGLTOKEN] [-a AKASHITOKEN] [-wid WORKSPACEID] [-b BREAKNUMBER] [-pid WORKINGPROJECTID] [-c COMPANYID] [-s START] [-e END]

optional arguments:
  -h, --help            show this help message and exit
  -t TOGGLTOKEN, --togglToken TOGGLTOKEN
                        Toggl Token
  -a AKASHITOKEN, --akashiToken AKASHITOKEN
                        Akashi Token
  -wid WORKSPACEID, --workspaceId WORKSPACEID
                        Workspace Id.
  -b BREAKNUMBER, --breakNumber BREAKNUMBER
                        Project number of break time.
  -pid WORKINGPROJECTID, --workingProjectId WORKINGPROJECTID
                        Working Project Number.
  -c COMPANYID, --companyId COMPANYID
                        Company Id.
  -s START, --start START
                        Start Date for auto input.
  -e END, --end END     End Date for auto input.
```

## copy-log.sh

This will collect your command log from logs folder using fzf command.
select your command and press Enter to get your previous command to your clipboard.
