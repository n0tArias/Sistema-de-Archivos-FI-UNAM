import struct

from .disk import CLUSTER_SIZE, FiUnamFSDisk
from .exceptions import SuperblockError

# Distribución binaria exacta de los primeros 64 bytes del cluster 0.
# Los 'x' son gaps de alineación que no transportan información.
_FMT = '<5x9s5s1x16s4xI6xI6xI'
_FMT_SIZE = struct.calcsize(_FMT)   # == 64

EXPECTED_FS_NAME = 'FiUnamFS'
EXPECTED_VERSION = '26-2'


class Superblock:
    def __init__(self, disk: FiUnamFSDisk) -> None:
        raw = disk.read_bytes(0, _FMT_SIZE)
        (
            fs_name_b, version_b, vol_label_b,
            self.cluster_size,
            self.dir_clusters,
            self.total_clusters,
        ) = struct.unpack(_FMT, raw)

        self.fs_name = fs_name_b.rstrip(b'\x00').decode('ascii')
        self.version = version_b.rstrip(b'\x00').decode('ascii')
        self.volume_label = (
            vol_label_b.rstrip(b'\x00').decode('ascii').strip()
        )
        self._validate()

    def _validate(self) -> None:
        if self.fs_name != EXPECTED_FS_NAME:
            raise SuperblockError(f"No es FiUnamFS: '{self.fs_name}'")
        if self.version != EXPECTED_VERSION:
            raise SuperblockError(
                f"Versión incompatible: '{self.version}' "
                f"(esperado '{EXPECTED_VERSION}')"
            )
        if self.cluster_size != CLUSTER_SIZE:
            raise SuperblockError(
                f"Tamaño de cluster inesperado: {self.cluster_size} B"
            )

    @property
    def data_start_cluster(self) -> int:
        return 1 + self.dir_clusters

    def __str__(self) -> str:
        return (
            f"FiUnamFS v{self.version}  «{self.volume_label}»  "
            f"cluster={self.cluster_size}B  "
            f"dir={self.dir_clusters}C  "
            f"total={self.total_clusters}C  "
            f"datos→C{self.data_start_cluster}"
        )
