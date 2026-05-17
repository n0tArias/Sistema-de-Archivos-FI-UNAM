from .directory import Directory
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
        raise NotImplementedError("Fase 4")

    # --- Fase 5 ---
    def rm(self, fs_name: str) -> None:
        raise NotImplementedError("Fase 5")

    def defrag(self) -> None:
        raise NotImplementedError("Fase 5")
