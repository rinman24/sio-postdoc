"""Encapsulate the `TransformationEngine`."""

from sio_postdoc.engine.transformation.contracts import MaskRequest
from sio_postdoc.engine.transformation.window import GridWindow

Mask = tuple[tuple[bool, ...]]
Values = tuple[tuple[int, ...]]


class TransformationEngine:
    """Define a `TransformationEngine` for analyzing time-height pixels."""

    def get_mask(self, request: MaskRequest) -> Mask:
        """Derive a mask based on the threashold."""
        window: GridWindow = GridWindow(length=request.length, height=request.height)
        mask: Mask = [
            [False for _ in range(len(request.values[0]))]
            for _ in range(len(request.values))
        ]
        horizontal: tuple[int, int] = (
            window.padding["left"],
            len(request.values) - window.padding["right"],
        )
        vertical: tuple[int, int] = (
            window.padding["bottom"],
            len(request.values[0]) - window.padding["top"],
        )
        for x in range(horizontal[0], horizontal[1]):
            for y in range(vertical[0], vertical[1]):
                window.position = (x, y)
                current_values: tuple[int, ...] = tuple(
                    request.values[i][j] for i, j in window.members()
                )
                # If the threshold is negative, flip min to max
                if request.threshold < 0:
                    current_values = tuple(
                        request.dtype.max if v == request.dtype.min else v
                        for v in current_values
                    )
                else:
                    current_values = tuple(
                        request.dtype.min if v == request.dtype.max else v
                        for v in current_values
                    )
                # Else, flip max to min
                if request.threshold < 0:
                    if any(
                        v / request.scale > request.threshold for v in current_values
                    ):
                        continue
                elif any(v / request.scale < request.threshold for v in current_values):
                    continue
                for i, j in window.members():
                    mask[i][j] = True
        return tuple(tuple(element) for element in mask)
