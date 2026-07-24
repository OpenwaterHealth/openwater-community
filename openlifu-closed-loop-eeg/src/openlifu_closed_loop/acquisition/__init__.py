"""EEG acquisition.

The acquisition layer is abstracted behind ``EEGSource`` so that a different amplifier
can be supported by implementing the interface and swapping in a new adapter, without
touching the rest of the pipeline. The reference adapter targets the g.tec g.Pipe SDK,
which is proprietary and user-supplied (see docs/hardware-setup.md); it is not vendored.

Contributions of adapters for other amplifiers are welcome — see docs/known-issues.md.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class EEGSource(ABC):
    """Interface every acquisition adapter implements."""

    @abstractmethod
    def start(self) -> None:
        """Begin streaming EEG samples onto the LSL 'EEG' stream."""

    @abstractmethod
    def stop(self) -> None:
        """Stop streaming and release the device."""


def check_gpipe() -> bool:
    """Return True if the proprietary g.Pipe SDK is importable in this environment.

    Scaffolding: the concrete g.Pipe adapter is migrated in with the developer's code.
    """
    raise NotImplementedError(
        "g.Pipe adapter is scaffolding pending code migration. Install the g.Pipe SDK "
        "per docs/hardware-setup.md, or use the synthetic source (no SDK required)."
    )
