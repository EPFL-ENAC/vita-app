from readers.Reader import Reader
from readers.Field import Field
from readers import patterns
from BoundingBox import BoundingBox


distinctivePattern = "EX500.+Treatment Report"


reader = Reader(
    "Alcon EX500",
    distinctivePattern,
    [
        Field("title", distinctivePattern),
        Field(
            "name",
            f"{patterns.name}, {patterns.name}",
            ["Last name", "First name"],
            below="title",
        ),
        Field(
            "birth date",
            patterns.date,
            ["Birth date"],
            region=BoundingBox.fromBounds(0.0, 0.5, 0.75, 1),
        ),
        Field("gender key", "Gender"),
        Field("gender", r"[a-z]+", ["Gender"], onRightof="gender key", regionWidth=10),
        Field("eye", "O[SD]", ["Eye"], region=BoundingBox.fromBounds(0.2, 0.7, 0.7, 1)),
        Field("treatment date key", "Treatment date"),
        Field(
            "treatment date",
            patterns.dateTime,
            ["Treatment date (DD.MM.YYYY)", "Treatment time"],
            onRightof="treatment date key",
            regionWidth=10,
        ),
        Field("refraction key", "Refraction"),
        Field(
            "refraction",
            patterns.shapeAlcon,
            ["Refraction sphere", "Refraction cylinder", "Refraction axis"],
            onRightof="refraction key",
            regionWidth=20,
        ),
        Field("treatment key", "(Treatment|Correction)", nCandidates=5),
        Field(
            "treatment",
            patterns.shapeAlcon,
            ["Treatment sphere", "Treatment cylinder", "Treatment axis"],
            onRightof="treatment key",
            regionWidth=20,
        ),
        Field("optical zone key", "Optical zone"),
        Field(
            "optical zone",
            patterns.lengthMm,
            ["Optical zone"],
            onRightof="optical zone key",
            regionWidth=5,
        ),
        Field("flap key", "(Flap / Epi Thickness|Planned flap)"),
        Field(
            "flap",
            patterns.lengthUm,
            ["Flap / Epi thickness"],
            onRightof="flap key",
            regionWidth=5,
        ),
        Field("transition zone key", "Transition zone"),
        Field(
            "transition zone",
            patterns.lengthMm,
            ["Transition zone"],
            onRightof="transition zone key",
            regionWidth=5,
        ),
        Field("cornea thickness key", "Cornea thickness"),
        Field(
            "cornea thickness",
            patterns.lengthUm,
            ["Cornea thickness"],
            onRightof="cornea thickness key",
            regionWidth=5,
        ),
        Field("ablation zone key", "Ablation zone"),
        Field(
            "ablation zone",
            patterns.lengthMm,
            ["Ablation zone"],
            onRightof="ablation zone key",
            regionWidth=5,
        ),
        Field("residual stroma key", "Residual stroma"),
        Field(
            "residual stroma",
            patterns.lengthUm,
            ["Residual stroma"],
            onRightof="residual stroma key",
            regionWidth=5,
        ),
        Field("total duration key", "Total duration"),
        Field(
            "total duration",
            patterns.timeS,
            ["Total duration (s)"],
            onRightof="total duration key",
            regionWidth=5,
        ),
        Field("breaks key", "Breaks"),
        Field(
            "breaks",
            rf"\d+ \({patterns.timeS}\)",
            ["Breaks (s)"],
            onRightof="breaks key",
            regionWidth=5,
        ),
        Field("k1q1 key", "K1 / Q1"),
        Field(
            "k1q1",
            patterns.KQ,
            ["K1", "K1 axis", "Q1"],
            onRightof="k1q1 key",
            regionWidth=20,
        ),
        Field("k2q2 key", "K2 / Q2"),
        Field(
            "k2q2",
            patterns.KQ,
            ["K2", "K2 axis", "Q2"],
            onRightof="k2q2 key",
            regionWidth=20,
        ),
        Field("pupil key", "Pupil"),
        Field(
            "pupil", patterns.lengthMm, ["Pupil"], onRightof="pupil key", regionWidth=5
        ),
    ]
)
