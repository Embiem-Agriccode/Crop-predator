# This is my first python prgram
from multiprocessing import reduction


print("Agriculture Farm Yeild")               
print("it should be my first project") 
# variables= A container for a value(String, intrgers, float, boolean)
#            A varieble behaves as it was the value it contains 
#Always remeber to add ----example; (f"My name is {first_name}") it is called the f_string and remeber that u only use F_string ONLY if we are adding veriable........... See Examples below

#strings- This is a klind of vareiable that contains an apostrophy 

first_name= "Mubarak Haruna"
Name_of_class= "level 2 student"
Choice="Agiculture"

   

print("--strings---")
print(f"His first name is {first_name}")
print(f"He is a {Name_of_class}")
print(f"He loves {Choice}")



#integers This kind of variables deals with whole numbers

Intergers="--integers---" 
no_of_farm_hecters= 4
No_Famers_Present= 28
No_Famers_Present= 4

print(Intergers)
print(f"Abdullathif used {no_of_farm_hecters} of farm land")
print(f"The farmers present was only {No_Famers_Present}")
print(f"He took the sun of only: {No_Famers_Present}hr")


 
#Float- This is a type of veriebles that has a decimal point------Examples;

lenth=4.6
Meters=9.89
Bags=15.3

print("--Float--")
print(f"The Farm was Very large that it contains {lenth}L")
print(f"It cost only few  bags, which were not more than {Bags} bags")

#boolean- This is a type of variebles that deals with the truth or false for example--IF(is used if
#  the qustion is True and remeber it starts with a capital letter T) likewise,
#  the ELSE(the qustion is False and remeber it starts with a capital letter F) E.g

boolean="--Belean--"
print(boolean)

school_boy = True 
if school_boy:
    print ("Yes he is in our class")
else:
    print ("Yes he is not in our class")   

Product_value= True

if Product_value: 
    print("This Product would be a problem solver in 30yrs to come")
else:
    print("This Product would be the problem in 30years to come")

Q=" What is respiration?"
print(Q)

which_is_correct= False
if which_is_correct:
    print("RESPIRATION IS THE PROCESS OF OXIDIZING AND DECOMPOZITION OF ORGANIC SUBSTANCE(EXPESIALLY SUGER SUCH AS " \
    "GLUCOSE WHICH)")
else:
    print("i don't know") 

    first_name= "Ibrahim masu'ud"
#typcating = This is the process of convertion one data type to other 
# E.g from float to integers---from boolean to strings or any type of conbination

#Implicite and Explicite

#Explicite (String, intrgers, float, boolean)
#Explicite
name = "mubarak"
age = 31
hecter = 8
Class_of_degree= True

if Class_of_degree:
    print("yeah that's true")
else:
    print("nah nt true")

type(name)
print(type(name))
print(type(age))
print(type(hecter))
print(type(Class_of_degree))

#This litraly shows the class of our data

#So now convert each data into other type

gpa = int(age)
print(gpa)

Class_of_degree = str(Class_of_degree)
print(Class_of_degree)

#Why should we convert to boolean----We could use type casting to see of somone has type their name or not and so on
# beware that this onl applies too strigs ("--")

name = bool (name)
print(name)

#Explicte Typecasting is when a value or variable is converted into a data type automaticlly (Math)

x = 2
y = 2.0

x = x / y
print(x)

#mad lips---This is a game that U have to fill in the blank------Plant discription

farmer= True
if farmer:
    print("Welcome, i am Embiem, i can help you wih any of your croop issue." \
    "Enter the information below")
else:
    print("Sorry, This site is only for Farmers")

Location=input ("Enter farm location: " )
Duration= int(input("Enter Yrs/Month/wk of farm: " ))
Yeild= int(input("Enter  the number of hecter: "))
plant1=input ("Enter the name of you plant you often plant: ")
plant2= input("Enter the name of the you have problems with: ")
problem= input ("Enter you problemin details: ")


print(f"I have a farm in {Location}.")
print(f"I have been farming for{Duration}yrs ")
print(f"The name of my plant is {plant1}, with {Yeild}s")
print(f"I have problem When it comes to planting {plant2}")
print(f"i wonder if u have a solution to this problem.{problem}")
print(f"Thank you, talk to you soon")

#area Calculation                                                   Would are use after words that ends with an ING (note that!!)
lenth= float(input("Enter you hecter lenth: "))
height= float(input("Enter the aree of your Hecter: "))

area= lenth * height

print(f"The area is {round(area, 3)}cm^2")
#Shopping cart

item= input("What item would like to buy: ")
price= float(input("What is the price? "))
quantity= int(input("How many do you want to buy?"))

total= price * quantity

print(f"You have purchased: {quantity} x {item}/s")
print(f"Your total is: N{round(total, 2)}")

#Somthing
name= input("Enter yoour name: ")
age= int(input("Enter you age: "))
age= age + 1
print (f"My name is{name}")
print (f"I am {age} years old")

#Mathimatics

yam= 4
yam += 6

# Whileloop this is a kinda loop that you cant get pass through wiithouth entering

name = input(" Enter you name: ")
if name == "":
    print("You did  not typr in your name! ")
else:
    print(f"Welcome {name}!, we are greatly happy u tried this app")

verb= input("Enter a verb: ")
adverb= input("Enter an adverb: ")
prepostion= input("Enter a prepostion: ")
 
print(f"One day i was {verb} alone, so ilu and i decided to with ilyasu. so {adverb} ")



# WEIGHT MEASURMENT
#weight = float(input("Enter the weight of your crop: "))
#height = float(input(""))

# Temprature conversion system 
#unit = (input("Choose the the unit of measurement Ferinite or celciuse (C/F): "))
#  temp = 9 * temp / 5 + 32
 #  print(f"The temprature in Fahrenheit is: {temp}F ")
#elif unit=="F":
 #  temp = round((temp - 32) * 5/9, 2)
  # print(f"The temprature in Celcius is: {temp}C")
#else:
 #  print(f"{unit} is not a unit of mesurement" )

#LOGICAL OPRATOR
#We Have AND (This is for know if smth is within a range) 
#OR(this is used to check if one condition is true)  
#NOT( this is used to flip the option the other way round)

room_temp= 323
heat = True
if room_temp > 0 or room_temp < 30:
   print("The temprature is good")
else: 
   print("The temprature is bad!")
temp1= 3
if temp1 >=0 or temp1 <=30:
   print("The temprature is  good!")
else:
   ("The temprature is bad")
if not heat:
   print("It is cold outside") 
else:print("It is hot outside")

#Temprature converter 2
unit= input("Enter the unit of your temprature (C/F): ")
temp= float(input("Enter the temprature: "))

if unit=="C":
      temp= round(temp -32 * 5/9, 2)
      print(f"The Temprature in Ferhenite is {temp}")
elif unit=="F":
      temp= round (temp * 32 /1.8, 2)
      print (f"The temprature in Celciusis {temp}")