import os

def select_script(op,cam_no):
    #docs = "cd Documents\OpenCV_Scripts"
    if op == "hsv":
        filename = "GetHSV.py"
    elif op == "screen":
        filename = "SelectScreen.py"
    elif op == "object":
        filename = "object_track.py"
    else:
        print "Can't find file. Retry"
        return 0
    run_script = "python %s --cam %d" % (filename, cam_no)
    #os.system(docs)
    os.system(run_script)

select_script('hsv',0)
