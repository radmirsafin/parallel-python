import os

program = "python"
print("Process calling")
arguments = ["called_process.py"]

os.execvp(program, (program,) + tuple(arguments))
print("Good Bye!!")
