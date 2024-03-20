from datetime import date

from sio_postdoc.engine.filtering.context import DateContext
from sio_postdoc.engine.filtering.strategies import NamesByDate

Content = tuple[str, ...]


class FilteringEngine:

    def __init__(self) -> None:
        self._date_context: DateContext = DateContext(NamesByDate())

    @property
    def date_context(self) -> DateContext:
        return self._date_context

    def apply(self, target: date, content: Content) -> Content:
        return self.date_context.apply(target=target, content=content)
