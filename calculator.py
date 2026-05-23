


# Simple Calculator

operator = input("Enter the operator (+ - * /): ")
num1 = float(input("Enter your 1st number: "))
num2 = float(input("Enter your 2nd number: "))

if operator =="+":
    print(num1 + num2)
elif operator =="*":
    print(num1 * num2)
elif operator =="/":
    print(num1 / num2)
elif operator =="-":
    print(num1 - num2)
else:
    print(f"{operator} is not a valid operator!")
   

name = input("Enter your name: ")

while name =="":
    print("You didn't type in your name! ")
    name = input("Enter your name: ")
    print(f"Welcome {name}!")
else :
    print("You entered the wrong age lad!")
    age= int(input("Enter your age: "))
print(f"You age {age} years old! welcome.")



age= int(input("Enter your age: "))
