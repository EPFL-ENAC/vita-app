from readers.Reader import Reader
from readers.Field import Field
from readers import patterns
from BoundingBox import BoundingBox


distinctivePattern = r"- Venue : \d+ / \d+"


# For paired fields, only define the keys first, values later
reader = Reader(
    "Sophtalmo",
    distinctivePattern,
    [
        Field(
            "nameBirth",
            fr" - {patterns.name} {patterns.name} - (\d+) - {patterns.date}",
            ["First name", "Last name", "ID", "DOB"],
            dataOrder=[1, 0, 3, 2]
        ),
        Field(
            "date",
            f"{patterns.date} .+ {distinctivePattern}",
            ["Date of consultation"]
        ),

        # Autorefractometer
        Field("autorefract", "AutoRéfractom"),
        Field(
            "autorefract OD key",
            "OD:",
            relativeTo="autorefract",
            # "Indice de fiabilité" may be present, extend search downwards
            regionRelative=BoundingBox.fromBounds(0, 30, -3.5, 0.5)
        ),
        Field(
            "autorefract OG key",
            "OG:",
            onRightof="autorefract OD key"
        ),

        # Refractometer
        Field("refraction", "Réfraction"),
        Field(
            "refraction OD key",
            "OD:",
            relativeTo="refraction",
            regionRelative=BoundingBox.fromBounds(0, 30, -2, 0.5)
        ),
        Field(
            "refraction OD ADD key",
            "Addition :",
            below="refraction OD key",
            regionHeight=2
        ),
        Field(
            "refraction OG key",
            "OG:",
            onRightof="refraction OD key"
        ),
        Field(
            "refraction OG ADD key",
            "Addition :",
            below="refraction OG key",
            regionHeight=2
        ),

        # Glasses
        Field("glasses", "Portée"),
        Field(
            "glasses OD key",
            "OD:",
            relativeTo="glasses",
            regionRelative=BoundingBox.fromBounds(0, 30, 0, 2)
        ),
        Field(
            "glasses OD ADD key",
            "Addition :",
            below="glasses OD key",
            regionHeight=2
        ),
        Field(
            "glasses OG key",
            "OG:",
            onRightof="glasses OD key"
        ),
        Field(
            "glasses OG ADD key",
            "Addition :",
            below="glasses OG key",
            regionHeight=2
        ),

        # Acuity
        Field(
            "acuity",
            "Acuité",
            below="refraction OD key",
            regionHeight=5
        ),
        Field(
            "acuity OD far key",
            "de loin",
            onRightof="acuity",
            regionWidth=50
        ),
        Field(
            "acuity OD near key",
            "de près",
            onRightof="acuity OD far key",
            regionWidth=50
        ),
        Field(
            "acuity OG far key",
            "de loin",
            onRightof="acuity OD near key" # search even if OD far not present
        ),
        Field(
            "acuity OG near key",
            "de près",
            onRightof="acuity OG far key"
        ),

        # IOP
        Field("IOP", r"^TO$"),
        Field(
            "IOP OD key",
            "OD:",
            relativeTo="IOP",
            regionRelative=BoundingBox.fromBounds(0, 30, -1.5, 0.5)
        ),
        Field(
            "IOP OG key",
            "OG:",
            onRightof="IOP OD key"
        ),
    ]
)


for eye in ["OD", "OG"]:
    reader.fields.extend([
        Field(
            f"autorefract {eye}",
            patterns.shapeSophtalmo,
            [
                f"{eye}-Autorefractometer-Sphere",
                f"{eye}-Autorefractometer-Cylindre",
                f"{eye}-Autorefractometer-Axis"
            ],
            onRightof=f"autorefract {eye} key",
            regionWidth=20
        ),
        Field(
            f"refraction {eye}",
            patterns.shapeSophtalmo,
            [
                f"{eye}-Refractometer-Sphere",
                f"{eye}-Refractometer-Cylindre",
                f"{eye}-Refractometer-Axis"
            ],
            onRightof=f"refraction {eye} key",
            regionWidth=20
        ),
        Field(
            f"refraction {eye} ADD",
            patterns.add,
            [f"{eye}-Refractometer-ADD"],
            onRightof=f"refraction {eye} ADD key",
            regionWidth=5
        ),
        Field(
            f"glasses {eye}",
            patterns.shapeSophtalmo,
            [
                f"{eye}-Glasses-Sphere",
                f"{eye}-Glasses-Cylindre",
                f"{eye}-Glasses-Axis"
            ],
            onRightof=f"glasses {eye} key",
            regionWidth=20
        ),
        Field(
            f"glasses {eye} ADD",
            patterns.add,
            [f"{eye}-Glasses-ADD"],
            onRightof=f"glasses {eye} ADD key",
            regionWidth=5
        ),
        Field(
            f"acuity {eye} far",
            patterns.acuityFar,
            [f"{eye}-VisualAcuity-Far"],
            below=f"acuity {eye} far key",
        ),
        Field(
            f"acuity {eye} near",
            patterns.acuityNear,
            [f"{eye}-VisualAcuity-Near"],
            below=f"acuity {eye} near key",
        ),
        Field(
            f"IOP {eye}",
            patterns.IOP,
            [f"{eye}-VisualAcuity-IOP"],
            onRightof=f"IOP {eye} key",
            regionWidth=5
        ),
    ])


# Keratometry

reader.fields.extend([
    Field("keratometry", "Kératométrie"),

    Field(
        "keratometry OD mm key",
        "mm",
        relativeTo="keratometry",
        regionRelative=BoundingBox.fromBounds(0, 30, -1.5, 0.5)
    ),
    Field(
        "keratometry OD As key",
        "As",
        onRightof="keratometry OD mm key",
        regionWidth=20
    ),
    Field(
        "keratometry OD Dio key",
        "Dio",
        onRightof="keratometry OD As key",
        regionWidth=20
    ),
    Field(
        "keratometry OD Javal key",
        "Javal",
        onRightof="keratometry OD Dio key",
        regionWidth=20
    ),

    Field(
        "keratometry OG mm key",
        "mm",
        onRightof="keratometry OD mm key",
    ),
    Field(
        "keratometry OG As key",
        "As",
        onRightof="keratometry OG mm key",
    ),
    Field(
        "keratometry OG Dio key",
        "Dio",
        onRightof="keratometry OG mm key",
    ),
    Field(
        "keratometry OG Javal key",
        "Javal",
        onRightof="keratometry OG mm key",
    ),
])


for eye in ["OD", "OG"]:
    for subIndex in range(4):
        sub = ["mm", "As", "Dio", "Javal"][subIndex]
        reps = [3, 3, 3, 2][subIndex]
        pattern = [
            patterns.keratoMm,
            patterns.keratoAs,
            patterns.keratoDio,
            patterns.keratoJaval
        ][subIndex]
        # for relative positioning
        referenceName = f"keratometry {eye} {sub} key"

        for i in range(1, reps + 1):  # from 1 to reps
            fieldName = f"keratometry {eye} {sub} {i}"

            # Need to adjust search region height because the reference "mm"
            # bbox is smaller than the others
            regionHeight = 2 if sub == "mm" and i == 1 else 1
            # Search further in case one OCR box is missing
            regionHeight *= reps + 1 - i  # from reps to 1

            reader.fields.append(
                Field(
                    fieldName,
                    pattern,
                    [f"{eye}-Keratometry-{sub}{i}"],
                    below=referenceName,
                    regionHeight=regionHeight
                )
            )
            # entries are stacked vertically, so the next one is below
            referenceName = fieldName
