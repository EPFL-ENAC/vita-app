import regex
from reader_scripts import patterns


def routine(pattern, string, groups=None):
    if groups is None:
        groups = (string,)

    match = regex.search(pattern, string)
    assert match is not None
    assert match.groups() == groups


def test_name():
    routine(patterns.name, "Alice-Bob Charlie")


def test_date():
    routine(patterns.date, "01.02.2003")
    routine(patterns.date, "01/02/2003")


def test_time():
    routine(patterns.time, "04:05")
    routine(patterns.time, "04:05:06")


def test_date_time():
    date = "01.02.2003"
    time = "04:05:06"
    string = f"{date} {time}"
    routine(patterns.date_time, string, (date, time))


def test_angle():
    routine(patterns.angle, "123 °", ("123",))


def test_shape_sphere():
    for s in ["+12.00", "+ 12.25", "-12.50", "- 12.75"]:
        routine(patterns.shape_sphere, s)


def test_shape_alcon():
    sphere = "- 4.50"
    cylinder = "- 0.25"
    axis = "170"
    string = f"{sphere} D {cylinder} D x {axis} °"
    routine(patterns.shape_alcon, string, (sphere, cylinder, axis))


def test_shape_sophtalmo():
    sphere = "-4.50"
    cylinder = "-0.25"
    axis = "170"
    string = f"{sphere} ( {cylinder} à {axis} °)"
    routine(patterns.shape_sophtalmo, string, (sphere, cylinder, axis))


def test_add():
    for s in ["0.00", "1.25", "2.50", "3.75"]:
        routine(patterns.add, s)


def test_acuity_far():
    # Test acuityFarMain
    for n in range(1, 10):  # 0.1 to 0.9
        routine(patterns.acuity_far, f"0.{n}")
    for n in [0.12, 0.25, 0.32, 0.63, 1.2, 1.25, 1.5, 1.6, 1.8]:
        routine(patterns.acuity_far, f"{n}")
    for n in [1, 2]:  # 1.0 and 2.0
        routine(patterns.acuity_far, f"{n:.1f}")
    for s in ["FC", "CLD", "CD", "CF", "HM", "VBLM", "VM", "MM"]:
        routine(patterns.acuity_far, s)
    for s1 in ["LP", "PL"]:
        for s2 in ["", "+", "-"]:
            routine(patterns.acuity_far, f"{s1}{s2}")

    # Test with acuityFarSub
    for s in [
        "3/5",
        "4/5",
        "5/5",
        "f",
        "ff",
        "+",
        "-",
        "--",
        "p",
        "pp",
        "faible",
    ]:
        routine(patterns.acuity_far, f"1.0 ({s})")
    pass


def test_acuity_near():  # Parinaud scale
    for n in [28, 1.5]:
        routine(patterns.acuity_near, f"P{n}f")


def test_IOP():
    routine(patterns.IOP, "12.3")
    routine(patterns.IOP, "APL15")
    routine(patterns.IOP, "APL")


def test_kerato_mm():
    for n in [7.00, 7.12, 7.89]:
        routine(patterns.kerato_mm, f"{n:.2f}")


def test_kerato_as():
    for n in [10, 175]:
        routine(patterns.kerato_as, f"{n}")


def test_kerato_dio():
    for n in [43, 44.25, 45.50, 46.75]:
        routine(patterns.kerato_dio, f"{n:.2f}")


def test_kerato_javal():
    for n in [-1, -2.25]:
        routine(patterns.kerato_javal, f"{n:.2f}")


def test_length_mm():
    routine(patterns.length_mm, "123.45 mm", ("123.45",))


def test_length_um():
    routine(patterns.length_um, "1234 um", ("1234",))


def test_time_s():
    routine(patterns.time_s, "123 s", ("123",))


def test_KQ():
    K = "123.45"
    KAxis = "123"
    Q = "123.45"
    string = f"{K} D @ {KAxis} ° / {Q}"
    routine(patterns.KQ, string, (K, KAxis, Q))
