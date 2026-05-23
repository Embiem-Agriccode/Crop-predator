#if = Do something like code if some condition is True
#Else do somthing else
#elif this can add as many else if as possible

#age= int(input("Enter your age: "))

#if age >= 100: 
   # print("You are to old for this")
#elif age >= 18:
   # print("You are now signed up!")
#elif age < 0:
   # print("You haven't been born yet!")
#else:
   # print("You must be 18+ to sign up")
 
print ("---Excercise---")


name= input(" Enter you name: ")
if name =="":
    print("You did  not typr in your name! ")
else:
    print(f"Hello, {name}!")

SoilpH1 = float(input("Enter your soil pH: "))
if SoilpH1 <= 0:
    print("This is an invalid soil pH")
elif SoilpH1 > 14:
    print(",This is an invalid soil pH!")
elif SoilpH1 < 5.5:
    print("Soil is too acidic for Maize! Recommend: Cassava or Sweet Potatoes")
elif SoilpH1 > 7.5:
    print("Soil is too alkaline for Maize! Recommend: Beans or Peas")
elif SoilpH1 >= 5.5 and SoilpH1 <= 7.5:
    print("Soil is suitable for Maize! Recommend: Maize or Sorghum")
elif SoilpH1 < 5.5:
    print("Soil is too acidic for Maize! Recommend: Cassava or Sweet Potatoes")
elif SoilpH1 <7:
    print(f"{SoilpH1}!, Your soil is acidic") 
elif SoilpH1 == 7:
    print("Your soil is neutral")
elif SoilpH1 > 7:
    print(",Your soil is alkaline")


#Conditional expresion 
#Formula x if condition else y


Crop = "miaze"
Heacters = 779
num = 20
Age = 3

#hevest = "" if Crop  else "poor yield"
#hecter = "Succesful" if Heacters > 100 else "Poor"
print("Adult" if Age >+18 else "You are not elgable for this coarse")
print("Even" if num > 2 else "ODD")