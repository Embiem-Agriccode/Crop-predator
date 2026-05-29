import pandas as pd
import matplotlib.pyplot as plt

# FUNCTION:
# With function — smart!
def check_ph(bu, ph, rn):
    print(bu  +"'s and the pH is: "+ str(ph)+" and the Farm size is: " + str(rn) )
# Now call it as many times as you want!
check_ph("Mubarak", 6.5, 7)
check_ph("Abubakar", 5.2, 7) 
check_ph("Fatima", 7.1, 9)

# Create a simple table (like Excel)
data = {
    "Crop":     ["Maize", "Rice", "Millet", "Cowpea"],
    "pH_Min":   [5.8,     5.5,    5.5,      6.0],
    "pH_Max":   [7.0,     6.5,    7.0,      7.0],
    "Yield":    [6,       7,      2,        2],
    "Price":    [120000,  400000, 200000,   450000]
}

# Create DataFrame (the table)
df = pd.DataFrame(data)

# Print the table
print(df)

# How many rows?
print(len(df))

# Show only the Crop column
print(df["Crop"])

# Show only crops with pH_Min less than 5.8
print(df[df["pH_Min"] < 5.8])

# Sort by Price (highest first)
print(df.sort_values("Price", ascending=False))

# Which crop has highest yield?
print(df[df["Yield"] == df["Yield"].max()])


# Read the CSV file
df2 = pd.read_csv("farms.csv")

# Show all farms
print(df2)

# Show only farms in Rainy Season
rain_season = df2[df2["Season"] == "Rainy Season"]
print("\nRainy Season Farms: ")
print(rain_season)

# show farm with good pH (btw 5.5 and 7.5)
good_pH = df2[(df2["pH"] >= 5.5) & (df2["pH"] <=7.5)]
print(good_pH)

# Avg pH of all farms
print("\nAvrage Soil pH: ")
avg =  df2["pH"].mean()
print(avg)

#Biggest farm
biggy = df2[df2["Size"] == df2["Size"].max()]
print("\nBiggest Farm: ")
print(biggy)

print()
# Add a new column — Revenue per hectare
df2["Revenue"] = df2["pH"] * 100000

#add colum that tell the useer about the pH
df2["pH_status"] = df2["pH"].apply(
    lambda x :"Good" if 5.5 <= x <=7.5 else "Bad"
)
print(df2)

df2 = pd.read_csv("result.csv")
# Save your results to a new CSV file
df2.to_csv("result.csv", index =False)
print("File saved!")

#Save only the good file
good_farms = df2[df2["pH_status"] == "Good"]
good_farms.to_csv("good_farms.csv", index=False)
print("Good farms saved!")




df2 = pd.read_csv("result.csv")

# Bar chart of farm sizes
df2.plot(
    kind="bar",
    x="Farm",
    y="Size",
    title="Farm Sizes in Nigeria",
    color="green"
)


plt.xlabel("Mubarak Farm")
plt.ylabel("Farm Size(hecter)")
plt.tight_layout()
plt.savefig("farm_chart.png")
print("Chart Save!")


print("=" * 40)
print("   FARM DATA ANALYSIS REPORT")
print("=" * 40)

#total farm(
print(f"\nTotal Farm: {len(df)}")
#avg farm
print(f"\nAvrage Soil pH: {df2["pH"].mean():.2f}")
#Biggest farm
print(f"\n Biggest Farm: {df2[df2["Size"] == df2["Size"].max()]["Farm"].values[0]}")
#samallest
print(f"\n Smallest Farm: {df2[df2["Size"] == df2["Size"].min()]["Farm"].values[0]}")

#pH status
df2["pH_status"] = df2["pH"].apply(
    lambda x: "Good" if 5.5 <= x <= 7.5 else "Bad"
)

print(df2)

good = df2[df2["pH_status"] == "Good"]
bad= df2[df2["pH_status"] == "Bad"]

print(f"\nGood pH farms: {good}")
print(f"\nBad pH farms: {bad}")

#Season Breakdown
print("\n Farm by season")
print (df2["Season"].value_counts())



good_farms = df2[df2["pH_status"] == "Good"]
good_farms.to_csv("good_farms.csv", index=False)
print("\nGood farms saved to good_farms.csv!")

#-------Draw chart--------

df2.plot(
    kind = "bar",
    x = "Location",
    y = "pH",
    title = "Mubarak's Farm",
    color = "green",
    legend = "False",
)

plt.xlabel("Location")
plt.ylabel("pH level")
plt.axhline(y=5.5, color="red", linestyle="--", label="Min pH")
plt.axhline(y=7.5, color="orange", linestyle="--", label="Max pH")
plt.savefig("ph_chart.png")
print("Chart saved as ph_chart.png!")

print("\n" + "=" * 40)
print("Analysis Complete")
print( "=" * 40)