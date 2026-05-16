from .directory import Directory
from .disk import FiUnamFSDisk
from .superblock import Superblock


class FiUnamFS:
    def __init__(self, disk: FiUnamFSDisk) -> None:
        self.disk = disk
        self.superblock = Superblock(disk)
        self.directory = Directory(disk, self.superblock)

    # --- Fase 3 ---
    def ls(self) -> None:
        raise NotImplementedError("Fase 3")

    def cp_out(self, fs_name: str, host_path: str) -> None:
        raise NotImplementedError("Fase 3")

    # --- Fase 4 ---
    def cp_in(self, host_path: str, fs_name: str) -> None:
        raise NotImplementedError("Fase 4")

    # --- Fase 5 ---
    def rm(self, fs_name: str) -> None:
        raise NotImplementedError("Fase 5")

    def defrag(self) -> None:
        raise NotImplementedError("Fase 5")
