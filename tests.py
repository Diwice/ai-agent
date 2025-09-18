from functions.run_python_file import *

testCases = [("calculator", "main.py"),("calculator", "main.py", ["3 + 5"]),("calculator", "tests.py"),("calculator", "../main.py"),("calculator", "nonexistent.py")]

for test in testCases :
	print(f"""Result for running {"'"+test[1]+"'" if test[1] != '.' else 'current'} file:\n"""+run_python_file(*test))
