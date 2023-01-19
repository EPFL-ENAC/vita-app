name = r"([a-zA-z\- ]+)"
date = r"(\d{2}\.\d{2}\.\d{4})"
time = r"(\d{2}:\d{2}:\d{2})"
dateTime = f"{date} {time}"
angle = r"(\d{1,3}) °"

shapeSphere = r"([+-] \d+\.\d{2}) D"
shapeCylinder = shapeSphere
shapeAxis = angle
shape = f"{shapeSphere} {shapeCylinder} x {shapeAxis}"

lengthMm = r"(\d+\.\d{2}) mm"
lengthUm = r"(\d{1,4}) [up]m"
timeS = r"(\d{1,3}) [sS]"

K = r"(\d+\.\d{2}) D"
KAxis = angle
Q = r"([+-]?\d+\.\d{2}|-+)"
KQ = f"{K} @ {KAxis} / {Q}"
