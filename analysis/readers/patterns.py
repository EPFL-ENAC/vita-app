name = r"([a-zA-z][a-zA-z\- ]*[a-zA-z])"
date = r"([0-3]\d[\./][0-1]\d[\./]\d{4})"
time = r"(\d{2}:\d{2}(?::\d{2})?)"
dateTime = f"{date} {time}"
angle = r"(\d{1,3}) °"

shapeSphere = r"([+-]? ?[1-3]?\d\.(?:00|25|50|75))"
shapeCylinder = shapeSphere
shapeAxis = angle
shapeAlcon = f"{shapeSphere} D {shapeCylinder} D x {shapeAxis}"
shapeSophtalmo = fr"{shapeSphere} \( ?{shapeCylinder} à {shapeAxis}\)"

add = r"([0-4]\.(?:00|25|50|75))"

acuityFarMain = r"(?:\d\.\d{1,2}|FC|CLD|CD|CF|HM|VBLM|VM|MM|(?:LP|PL)[\+\-]?)"
acuityFarSub = r"(?:3/5|4/5|5/5|f|ff|\+|-|--|p|pp|faible)"
acuityFar = fr"({acuityFarMain}(?: \({acuityFarSub}\))?)"

acuityNear = r"(P\d{1,2}(?:\.\d)?f)"
IOP = r"([(?:APL)(?:\d{1,2}(?:\.\d))]+)"

keratoMm = r"(\d\.\d{2})"
keratoAs = r"(\d{1,3})"
keratoDio = r"(\d{1,2}\.(?:00|25|50|75))"
keratoJaval = r"([+-]\d\.(?:00|25|50|75))"

lengthMm = r"(\d+\.\d{2}) mm"
lengthUm = r"(\d{1,4}) [up]m"
timeS = r"(\d{1,3}) [sS]"

K = r"(\d+\.\d{2}) D"
KAxis = angle
Q = r"([+-]?\d+\.\d{2}|-+)"
KQ = f"{K} @ {KAxis} / {Q}"
