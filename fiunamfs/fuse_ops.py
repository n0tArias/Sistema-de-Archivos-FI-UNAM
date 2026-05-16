from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .filesystem import FiUnamFS


class FiUnamFSFuse:
    """Fase 6: puente entre FUSE y FiUnamFS."""

    def __init__(self, fs: FiUnamFS) -> None:
        self._fs = fs

    def mount(self, mountpoint: str, foreground: bool = True) -> None:
        raise NotImplementedError("Fase 6")
