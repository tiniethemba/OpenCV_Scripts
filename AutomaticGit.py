import subprocess
import time
import os


project_end = "2018-05-11"


#bash_path = "C:\Program Files\Git\git-bash.exe"
bash_add_commit = "git add . && git commit -am 'This is the automated git script'"
countno = 1
gitadd = "git add -A"
gitcommit = "git commit -m This is the automated commit #%d" % countno
gitpush = "git push"


while True:
    current_date = time.strftime("%Y-%m-%d")
    if current_date == project_end:
        break
    else:
        os.system()
    time.sleep(60*60*12)
    countno += 1


