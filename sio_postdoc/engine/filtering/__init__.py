"""Initialize the Filering Engine."""

from typing import Union

from sio_postdoc.engine.transformation.contracts import InstrumentData

ContentType = Union[str, bool, InstrumentData]
Content = tuple[ContentType, ...]

Mask = tuple[int, ...]
