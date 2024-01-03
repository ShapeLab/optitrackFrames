import subprocess
import sys
import threading

# def processFrame(frame)

def processStream(text):
    lines = text.splitlines()
    endPoint = -1
    startPoint = -1
    for i in range(len(lines) - 1, 0, -1):
        l = lines[i]
        if l == "MoCap Frame End":
            print("found frame")
            endPoint = i
            break

    for j in range(endPoint, 0, -1):
        l = lines[j]
        if l == "MoCap Frame Begin":
            startPoint = j
            break
    
    print(f"Last Frame Start: {startPoint}, End: {endPoint}")
    return "\n".join(lines[startPoint:endPoint+1])
                

recentText = ""
def on_timeout(proc, status_dict):
    status_dict['timeout'] = True
    proc.kill()

status_dict = {'timeout':False}
p = subprocess.Popen(["python", "C:.\PythonClient\PythonSample.py"], stdout=subprocess.PIPE)
recentText = p.stdout.read1().decode("utf-8")
timer = threading.Timer(1, on_timeout, (p, status_dict))
timer.start()
p.wait()
timer.cancel()

print(processStream(recentText))
