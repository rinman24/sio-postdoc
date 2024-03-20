"""Transformation Engine Strategies."""

# import dataclasses
from abc import ABC  # , abstractmethod


# Define a protocol or an ABC depending on the use case later
class AbstractUnpackingStrategy(ABC):
    pass


class SHEBA_DABUL(AbstractUnpackingStrategy):

    def unpack(self):
        """Here is where we will unpack the SHEBA BABUL Stuff."""
        """But first, I need to create two test files, that act like the sheba data"""
        """for now I will keep the code in this module, but it will need to be put somewhere else later"""
