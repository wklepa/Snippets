"""
Code snippet to accept the default choice if no input is provided.
"""

defaultChoice: str = "my_option"

userInput: str = input(
    f'Input choice or press enter to accept "{defaultChoice}": '
).strip()
if userInput == "":
    userInput = defaultChoice

print(userInput)
