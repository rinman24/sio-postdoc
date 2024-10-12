"""TODO: These probably belog somewhere else."""


def _convert_bytes(value: bytes | float) -> int:
    result: int
    try:
        result = int.from_bytes(value)
    except TypeError:
        result = 0
    return result
