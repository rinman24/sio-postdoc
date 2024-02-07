from pathlib import Path

MONTH_DIRECTORIES: dict[int, str] = {
    1: "01-january",
    2: "02-february",
    3: "03-march",
    4: "04-april",
    5: "05-may",
    6: "06-june",
    7: "07-july",
    8: "08-august",
    9: "09-september",
    10: "10-october",
    11: "11-november",
    12: "12-december",
}

# TODO: Move this to config
DATADIR: Path = Path("/Users/richardinman/Code/sio-postdoc/sio_postdoc/data")

VALID_LOCATIONS: set[str] = set(
    [
        "sheba",
    ]
)

VALID_NAMES: set[str] = set(
    [
        "lidar",
    ]
)
