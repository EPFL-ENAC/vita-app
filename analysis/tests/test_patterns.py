import context
from readers import patterns
import regex


def routine(pattern, string, groups=None):
    if groups is None:
        groups = (string,)

    match = regex.search(pattern, string)
    assert match is not None
    assert match.groups() == groups


def testName():
    routine(patterns.name, "Alice-Bob Charlie")


def testDate():
    routine(patterns.date, "01.02.2003")
    routine(patterns.date, "01/02/2003")


def testTime():
    routine(patterns.time, "04:05")
    routine(patterns.time, "04:05:06")


def testDateTime():
    date = "01.02.2003"
    time = "04:05:06"
    string = f"{date} {time}"
    routine(patterns.dateTime, string, (date, time))


def testAngle():
    routine(patterns.angle, "123 °", ("123",))


def testShapeSphere():
    for s in ["+12.00", "+ 12.25", "-12.50", "- 12.75"]:
        routine(patterns.shapeSphere, s)


def testShapeAlcon():
    sphere = "- 4.50"
    cylinder = "- 0.25"
    axis = "170"
    string = f"{sphere} D {cylinder} D x {axis} °"
    routine(patterns.shapeAlcon, string, (sphere, cylinder, axis))


def testShapeSophtalmo():
    sphere = "-4.50"
    cylinder = "-0.25"
    axis = "170"
    string = f"{sphere} ( {cylinder} à {axis} °)"
    routine(patterns.shapeSophtalmo, string, (sphere, cylinder, axis))


def testAdd():
    for s in ["0.00", "1.25", "2.50", "3.75"]:
        routine(patterns.add, s)


def testAcuityFar():
    # Test acuityFarMain
    for n in range(1, 10):  # 0.1 to 0.9
        routine(patterns.acuityFar, f"0.{n}")
    for n in [0.12, 0.25, 0.32, 0.63, 1.2, 1.25, 1.5, 1.6, 1.8]:
        routine(patterns.acuityFar, f"{n}")
    for n in [1, 2]:  # 1.0 and 2.0
        routine(patterns.acuityFar, f"{n:.1f}")
    for s in ["FC", "CLD", "CD", "CF", "HM", "VBLM", "VM", "MM"]:
        routine(patterns.acuityFar, s)
    for s1 in ["LP", "PL"]:
        for s2 in ["", "+", "-"]:
            routine(patterns.acuityFar, f"{s1}{s2}")

    # Test with acuityFarSub
    for s in ["3/5", "4/5", "5/5", "f", "ff", "+", "-", "--", "p", "pp", "faible"]:
        routine(patterns.acuityFar, f"1.0 ({s})")
    pass


def testAcuityNear():  # Parinaud scale
    for n in [28, 1.5]:
        routine(patterns.acuityNear, f"P{n}f")


def testIOP():
    routine(patterns.IOP, "12.3")
    routine(patterns.IOP, "APL15")
    routine(patterns.IOP, "APL")


def testKeratoMm():
    for n in [7.00, 7.12, 7.89]:
        routine(patterns.keratoMm, f"{n:.2f}")


def testKeratoAs():
    for n in [10, 175]:
        routine(patterns.keratoAs, f"{n}")


def testKeratoDio():
    for n in [43, 44.25, 45.50, 46.75]:
        routine(patterns.keratoDio, f"{n:.2f}")


def testKeratoJaval():
    for n in [-1, -2.25]:
        routine(patterns.keratoJaval, f"{n:.2f}")


def testLengthMm():
    routine(patterns.lengthMm, "123.45 mm", ("123.45",))


def testLengthUm():
    routine(patterns.lengthUm, "1234 um", ("1234",))


def testTimeS():
    routine(patterns.timeS, "123 s", ("123",))


def testKQ():
    K = "123.45"
    KAxis = "123"
    Q = "123.45"
    string = f"{K} D @ {KAxis} ° / {Q}"
    routine(patterns.KQ, string, (K, KAxis, Q))
