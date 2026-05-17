import math
import os

from .directory import Directory, DirectoryEntry
from .disk import CLUSTER_SIZE, FiUnamFSDisk
from .exceptions import FilesystemError
from .superblock import Superblock


class FiUnamFS:
    def __init__(self, disk: FiUnamFSDisk) -> None:
        self.disk = disk
        self.superblock = Superblock(disk)
        self.directory = Directory(disk, self.superblock)

    # --- Fase 3 ---
    def ls(self) -> None:
        files = self.directory.list_files()
        if not files:
            print("(directorio vacío)")
            return
        header = f"{'Nombre':<15}  {'Tamaño':>10}  {'C.Inicio':>8}  Modificado"
        print(header)
        print('-' * len(header))
        for e in files:
            mtime = e.modified_at if e.modified_at else '?'
            print(
                f"{e.name:<15}  {e.size:>10} B  "
                f"{e.start_cluster:>8}  {mtime}"
            )

    def cp_out(self, fs_name: str, host_path: str) -> None:
        entry = self.directory.find(fs_name)
        if entry is None:
            raise FilesystemError(f"Archivo no encontrado: '{fs_name}'")

        remaining = entry.size
        with open(host_path, 'wb') as out:
            for c in range(
                entry.start_cluster,
                entry.start_cluster + entry.clusters_needed(),
            ):
                block = self.disk.read_cluster(c)
                # El último cluster puede tener padding nulo; se recorta
                # al mínimo entre CLUSTER_SIZE y los bytes que faltan.
                out.write(block[:remaining])
                remaining -= CLUSTER_SIZE

    # --- Fase 4 ---
    def cp_in(self, host_path: str, fs_name: str) -> None:
        if not os.path.exists(host_path):
            raise FilesystemError(f"Archivo no encontrado: '{host_path}'")

        size = os.path.getsize(host_path)

        if self.directory.find(fs_name) is not None:
            raise FilesystemError(f"'{fs_name}' ya existe en el sistema")

        clusters_needed = math.ceil(size / CLUSTER_SIZE) if size else 0

        start = self.directory.find_contiguous_clusters(clusters_needed)
        if start is None:
            raise FilesystemError(
                "Espacio contiguo insuficiente. "
                "Sugerencia: intente ejecutar -defrag"
            )

        entry = DirectoryEntry.new_file(fs_name, size, start)
        self.directory.add_entry(entry)

        with open(host_path, 'rb') as src:
            for current_cluster in range(start, start + clusters_needed):
                chunk = src.read(CLUSTER_SIZE)
                self.disk.write_cluster(
                    current_cluster,
                    chunk.ljust(CLUSTER_SIZE, b'\x00'),
                )

    # --- Fase 5 ---
    def rm(self, fs_name: str) -> None:
        raise NotImplementedError("Fase 5")

    def defrag(self) -> None:
        raise NotImplementedError("Fase 5")
