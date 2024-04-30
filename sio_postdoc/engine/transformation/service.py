"""Encapsulate the `TransformationEngine`."""

from sio_postdoc.engine.transformation.window import GridWindow

Mask = tuple[tuple[bool, ...]]
Values = tuple[tuple[int]]


class TransformationEngine:
    """Define a `TransformationEngine` for analyzing time-height pixels."""

    def get_mask(self, values: Values, window: GridWindow, threshold: int) -> Mask:
        """Derive a mask based on the threashold."""
        mask: Mask = [
            [False for _ in range(len(values[0]))] for _ in range(len(values))
        ]
        horizontal: tuple[int, int] = (
            window.padding["left"],
            len(values) - window.padding["right"],
        )
        vertical: tuple[int, int] = (
            window.padding["bottom"],
            len(values[0]) - window.padding["top"],
        )
        for x in range(horizontal[0], horizontal[1]):
            for y in range(vertical[0], vertical[1]):
                window.position = (x, y)
                if any(values[i][j] < threshold for i, j in window.members()):
                    continue
                for i, j in window.members():
                    mask[i][j] = True
        return tuple(tuple(element) for element in mask)
