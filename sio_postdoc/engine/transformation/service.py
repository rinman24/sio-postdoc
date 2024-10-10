"""Encapsulate the `TransformationEngine`."""

from typing import Callable

from typing_extensions import deprecated

from sio_postdoc.engine import DType
from sio_postdoc.engine.transformation.contracts import Direction, MaskRequest
from sio_postdoc.engine.transformation.window import GridWindow

MASK_TYPE: DType = DType.I1

Mask = tuple[tuple[int, ...], ...]


class TransformationEngine:
    """Define a `TransformationEngine` for analyzing time-height pixels."""

    @deprecated("You no longer use this workflow.")
    def get_mask(self, request: MaskRequest) -> Mask:
        """Derive a mask based on the threashold."""
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
        # Set up the threshold direciton
        match request.threshold.direction:
            case Direction.LESS_THAN:
                mask_method: Callable = self._max_threshold_mask
            case Direction.GREATER_THAN:
                mask_method: Callable = self._min_threshold_mask
        for x in range(horizontal[0], horizontal[1]):
            for y in range(vertical[0], vertical[1]):
                window.position = (x, y)
                current_values: tuple[int, ...] = tuple(
                    request.values[i][j] for i, j in window.members()
                )
                # This is the problem is that you're checking for the mins...
                if any(v == request.dtype.min for v in current_values):
                    mask_value: int = MASK_TYPE.min
                else:
                    mask_value: int = mask_method(
                        request.scale, request.threshold.value, current_values
                    )
                for i, j in window.members():
                    mask[i][j] = mask_value
        return tuple(tuple(element) for element in mask)

    @staticmethod
    def _max_threshold_mask(
        scale: int, threshold: int, current_values: tuple[int, ...]
    ) -> int:
        return 1 if all(v / scale < threshold for v in current_values) else 0

    @staticmethod
    def _min_threshold_mask(
        scale: int, threshold: int, current_values: tuple[int, ...]
    ) -> int:
        return 1 if all(threshold < v / scale for v in current_values) else 0
