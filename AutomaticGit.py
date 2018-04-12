import subprocess
import time


project_end = "2018-05-11"


#bash_path = "C:\Program Files\Git\git-bash.exe"
bash_add_commit = "git add . && git commit -am 'This is the automated git script'"


while True:
    current_date = time.strftime("%Y-%m-%d")
    if current_date == project_end:
        break
    subprocess.Popen(bash_add_commit, shell=True, executable=bash_path)


