"""Random bag with previews."""

import random
from collections import deque
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from common.enum import Mino
    from model.ruleset import Ruleset


@dataclass
class Bag:
    """Random bag with previews."""

    ruleset: InitVar["Ruleset"]

    previews: "deque[Mino]" = field(init=False)
    _generator: "RandomBag" = field(init=False)

    def __post_init__(self, ruleset) -> None:
        self.previews = deque([], maxlen=ruleset.num_previews)
        self._generator = iter(RandomBag(ruleset.mino_types))
        self._refill(ruleset.num_previews)

    @property
    def next(self) -> "Mino":
        """The next mino in the bag."""
        num_previews = len(self.previews)
        mino = self.previews.popleft()
        self._refill(num_previews)

        return mino

    def _refill(self, num_previews: int) -> None:
        while len(self.previews) < num_previews:
            self.previews.append(next(self._generator))


@dataclass
class RandomBag:
    """Endless bag of minos which shuffles when a full bag has been read."""

    _source: "list[Mino]"
    _index: int = field(default=0, init=False)
    _size: int = field(init=False)

    def __post_init__(self):
        self._size = len(self._source)
        random.shuffle(self._source)

    def __iter__(self) -> "RandomBag":
        self._index = 0
        return self

    def __next__(self) -> "Mino":
        mino = self._source[self._index]
        self._index = (self._index + 1) % self._size
        if self._index == 0:
            random.shuffle(self._source)

        return mino
