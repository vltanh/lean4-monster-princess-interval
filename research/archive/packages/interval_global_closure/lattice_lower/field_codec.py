#!/usr/bin/env python3
"""Lossless storage of the frozen symmetric, outward-after-two lattice CDF.

The compact gzip payload has a <IIIIQ header: version 2, B, 2B+1, B+1, D.
For times 0 through 2 it stores the B nonnegative uint16 differences between
successive positive-half CDF numerators, starting from the center value D/2.
Reflection and the exact outward shift determine all omitted table entries.
Expansion produces the version-1 uint64 table read by the C++ verifier.
No floating-point arithmetic or discovery-field interpolation is used.
"""
from array import array
import argparse
import gzip
import hashlib
from pathlib import Path
import struct
import sys


def little_bytes(values, kind):
    data = array(kind, values)
    if sys.byteorder != 'little':
        data.byteswap()
    return data.tobytes()


def decode(raw, kind):
    data = array(kind)
    data.frombytes(raw)
    if sys.byteorder != 'little':
        data.byteswap()
    return data


def expand(source, destination):
    digest = hashlib.sha256()
    with gzip.open(source, 'rb') as src, open(destination, 'wb') as dst:
        header = src.read(24)
        assert len(header) == 24, 'truncated compact header'
        version, B, rows, columns, D = struct.unpack('<IIIIQ', header)
        assert version == 2 and B > 0 and B % 2 == 0
        assert rows == 2 * B + 1 and columns == B + 1
        assert 0 < D <= 131070 and D % 2 == 0

        def write(raw):
            digest.update(raw)
            dst.write(raw)

        write(struct.pack('<IIIIQ', 1, B, 6 * B + 1, 2 * B + 1, D))
        positive = None
        for n in range(6 * B + 1):
            if n <= 2 * B:
                raw = src.read(2 * B)
                assert len(raw) == 2 * B, 'truncated compact row'
                positive = [D // 2]
                for increment in decode(raw, 'H'):
                    positive.append(positive[-1] + increment)
                assert positive[-1] <= D, 'CDF outside [0,1]'
            else:
                positive = [D // 2] + positive[:-1]
            row = [D - a for a in positive[:0:-1]] + positive
            write(little_bytes(row, 'Q'))
        assert src.read(1) == b'', 'unexpected compact trailing data'
    return digest.hexdigest()


def pack(source, destination):
    with open(source, 'rb') as src, open(destination, 'wb') as raw_dst:
        header = src.read(24)
        version, B, rows, columns, D = struct.unpack('<IIIIQ', header)
        assert version == 1 and rows == 6 * B + 1 and columns == 2 * B + 1
        assert B > 0 and B % 2 == 0 and 0 < D <= 131070 and D % 2 == 0
        with gzip.GzipFile(fileobj=raw_dst, mode='wb', filename='', mtime=0) as dst:
            dst.write(struct.pack('<IIIIQ', 2, B, 2 * B + 1, B + 1, D))
            for n in range(2 * B + 1):
                raw = src.read(8 * columns)
                assert len(raw) == 8 * columns, 'truncated full row'
                row = decode(raw, 'Q')
                assert row[B] == D // 2
                assert all(row[j] + row[2 * B - j] == D for j in range(B))
                increments = [row[j + 1] - row[j] for j in range(B, 2 * B)]
                assert all(0 <= a <= 65535 for a in increments)
                assert row[-1] <= D
                dst.write(little_bytes(increments, 'H'))
    # A round-trip hash comparison with the full input is required before
    # accepting a packed certificate; the replay manifest binds that hash.
    return hashlib.sha256(Path(destination).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['pack', 'expand'])
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    print((pack if args.operation == 'pack' else expand)(args.source, args.destination))


if __name__ == '__main__':
    main()
