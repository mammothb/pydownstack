"""Random bag with previews."""

import random
from collections import deque
from dataclasses import InitVar, dataclass, field

from model.polymino import Mino
from model.ruleset import Ruleset


@dataclass
class Bag:
    """Random bag with previews."""

    ruleset: InitVar[Ruleset]

    previews: deque[Mino] = field(init=False)
    source: "RandomBag" = field(init=False)

    def __post_init__(self, ruleset) -> None:
        self.previews = deque([], maxlen=ruleset.num_previews)
        self.source = iter(RandomBag(ruleset.mino_types))
        self._refill(ruleset.num_previews)

    @property
    def next(self) -> Mino:
        """The next mino in the bag."""
        num_previews = len(self.previews)
        mino = self.previews.popleft()
        self._refill(num_previews)

        return mino

    def _refill(self, num_previews: int) -> None:
        while len(self.previews) < num_previews:
            self.previews.append(next(self.source))


@dataclass
class RandomBag:
    """Endless bag of minos which shuffles when a full bag has been read."""

    source: list[Mino]
    index: int = field(default=0, init=False)
    size: int = field(init=False)

    def __post_init__(self):
        self.size = len(self.source)
        random.shuffle(self.source)

    def __iter__(self) -> "RandomBag":
        self.index = 0
        return self

    def __next__(self) -> Mino:
        mino = self.source[self.index]
        self.index = (self.index + 1) % self.size
        if self.index == 0:
            random.shuffle(self.source)

        return mino
