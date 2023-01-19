import sys

sys.path.insert(0, ".")

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


def testTime():
    routine(patterns.time, "04:05:06")


def testDateTime():
    date = "01.02.2003"
    time = "04:05:06"
    string = f"{date} {time}"
    routine(patterns.dateTime, string, (date, time))


def testAngle():
    routine(patterns.angle, "123 °", ("123",))


def testShapeSphere():
    routine(patterns.shapeSphere, "+ 123.45 D", ("+ 123.45",))
    routine(patterns.shapeSphere, "- 1.23 D", ("- 1.23",))


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
