#!/usr/bin/env python3
import sys
import argparse

from fiunamfs import FiUnamFSDisk, FiUnamFS, FiUnamFSError


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog='main.py',
        description='FiUnamFS — sistema de archivos de asignación contigua',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument('imagen', metavar='IMG',
                   help='Ruta al archivo .img de FiUnamFS')

    ops = p.add_mutually_exclusive_group(required=True)
    ops.add_argument('-ls', action='store_true',
                     help='Listar contenidos del directorio')
    ops.add_argument('-cp_out', nargs=2,
                     metavar=('NOMBRE', 'DESTINO'),
                     help='Copiar archivo de FiUnamFS al host')
    ops.add_argument('-cp_in', nargs=2,
                     metavar=('ORIGEN', 'NOMBRE'),
                     help='Copiar archivo del host a FiUnamFS')
    ops.add_argument('-rm', metavar='NOMBRE',
                     help='Eliminar archivo del sistema')
    ops.add_argument('-defrag', action='store_true',
                     help='Compactar espacio libre')
    ops.add_argument('-mount', metavar='PUNTO',
                     help='Montar con FUSE en punto de montaje')
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        with FiUnamFSDisk(args.imagen) as disk:
            fs = FiUnamFS(disk)

            if args.ls:
                fs.ls()
            elif args.cp_out:
                fs.cp_out(args.cp_out[0], args.cp_out[1])
            elif args.cp_in:
                fs.cp_in(args.cp_in[0], args.cp_in[1])
            elif args.rm:
                fs.rm(args.rm)
            elif args.defrag:
                fs.defrag()
            elif args.mount:
                from fiunamfs.fuse_ops import FiUnamFSFuse
                FiUnamFSFuse(fs).mount(args.mount)

    except FiUnamFSError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
