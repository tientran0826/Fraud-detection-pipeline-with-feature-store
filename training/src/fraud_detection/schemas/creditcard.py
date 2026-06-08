class CreditCardSchema:

    TARGET = "Class"

    COLUMNS = {
        "Time": "float64",
        **{f"V{i}": "float64" for i in range(1, 29)},
        "Amount": "float64",
        "Class": "int64",
    }

    REQUIRED_COLUMNS = list(COLUMNS.keys())

    @classmethod
    def features(cls) -> list[str]:
        return [column for column in cls.COLUMNS if column != cls.TARGET]
