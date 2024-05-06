"""Encapsulate the `TransformationEngine`."""

from sio_postdoc.engine import DType
from sio_postdoc.engine.transformation.contracts import MaskRequest
from sio_postdoc.engine.transformation.window import GridWindow

MASK_TYPE: DType = DType.I1

Mask = tuple[tuple[int, ...], ...]


class TransformationEngine:
    """Define a `TransformationEngine` for analyzing time-height pixels."""

    def get_mask(self, request: MaskRequest) -> Mask:
        """Derive a mask based on the threashold."""
        mask_value: int
        window: GridWindow = GridWindow(length=request.length, height=request.height)
        mask: Mask = [
            [0 for _ in range(len(request.values[0]))]
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
                if any(v == request.dtype.min for v in current_values):
                    mask_value = MASK_TYPE.min
                elif request.threshold < 0:
                    mask_value = (
                        1
                        if all(
                            v / request.scale < request.threshold
                            for v in current_values
                        )
                        else 0
                    )
                else:  # 0 <= request.threshold
                    mask_value = (
                        1
                        if all(
                            request.threshold < v / request.scale
                            for v in current_values
                        )
                        else 0
                    )
                for i, j in window.members():
                    mask[i][j] = mask_value
        return tuple(tuple(element) for element in mask)
