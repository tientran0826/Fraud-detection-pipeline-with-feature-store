class CreditCardSchema:

    TARGET = "Class"

    FEATURES = [
        "Time",
        *[f"V{i}" for i in range(1, 29)],
        "Amount",
    ]

    REQUIRED_COLUMNS = FEATURES + [TARGET]
