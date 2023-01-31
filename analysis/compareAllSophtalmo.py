from os import system

for i in range(1, 11):
    for app in ["", ".2"]:
        filename = f"patient{i}{app}"
        cmd = f"python3 compare.py references/sophtalmo-screenshots/{filename}.xlsx outputs/sophtalmo-screenshots/{filename}.csv"
        system(cmd)
