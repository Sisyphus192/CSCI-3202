import subprocess

output = subprocess.check_output('python autograder.py -q q1 --no-graphics | grep Average', shell=True).decode('utf-8')
o = output.split(':')[1]
print(o)