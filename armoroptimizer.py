import pandas as pd

# Loads the Excel file.
xls = pd.ExcelFile("armors.xlsx")
hats = pd.read_excel(xls, "Hats").to_dict("records")
chests = pd.read_excel(xls, "Chests").to_dict("records")
gauntlents = pd.read_excel(xls, "Gauntlets").to_dict("records")
pants = pd.read_excel(xls, "Pants").to_dict("records")

# Gets the maximum possible weight and the stat to maximize.
weight = input("Introduce the maximum weight you can use for your armor: ")
print("Introduce the stat you want to maximize: ")
print("1. Physical defence 2. Strike defence 3. Slash defence")
print("4. Pierce defence 5. Magic resistance 6. Fire resistance")
print("7. Lit resistance 8. Holy resistance 9. Immunity")
sel = input("10. Robustness 11. Focus 12. Vitality 13. Poise\n")

maxparam = [
    "Phy",
    "VS Strike",
    "VS Slash",
    "VS Pierce",
    "Mag",
    "Fir",
    "Lit",
    "Hol",
    "Immunity",
    "Robustness",
    "Focus",
    "Vitality",
    "Poise",
][int(sel) - 1]

best = -1.0
bestArmor = []
# Terribly written function which can be optimized in a thousand ways but will do the work as a 10 minutes script.
# Takes several minutes to complete, around 10-15 on my pc.
# Iterates through every single possible combination of armors in the game and gets the one with the max stat.
# Should be rewritten to only check viable options instead of every single one. A bit less accuracy but much faster results.
# If this was to be implemented to be used by multiple people, the results should be stored on a data structure to be accessed later directly.
for hat in hats:
    for chest in chests:
        for gauntlet in gauntlents:
            for pant in pants:
                cweight = pant["Wgt"] + gauntlet["Wgt"] + chest["Wgt"] + hat["Wgt"]
                if cweight < float(weight):
                    value = (
                        float(pant[maxparam])
                        + float(gauntlet[maxparam])
                        + float(chest[maxparam])
                        + float(hat[maxparam])
                    )
                    if value > best:
                        best = value
                        bestArmor = [hat["Name"], chest["Name"], gauntlet["Name"], pant["Name"]]
for x in bestArmor:
    if x:
        print(x.title())
print("The maximum attainable stat your armor can get is : " + str(best))
