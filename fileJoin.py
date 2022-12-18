import pandas as pd
import glob

files = glob.glob(r'C:\Users\jbbla\OneDrive\Documents\Races2018//*.csv')

allRaces = pd.DataFrame()

for file in files:
    df = pd.read_csv(file)
    allRaces = pd.concat([allRaces, df])

dir = str(r"C:\Users\jbbla\OneDrive\Documents\concatRaces" + "\\" + "races2018" + ".csv")
allRaces.to_csv(dir)

print(allRaces.head)
print("Complete Conversion")

    

