"""Read a binary file in chunks, using 'modern' idiomatic Python."""
import functools

CHUNKSIZE = 42

with open(__file__, 'rb') as handle:
    read_chunk = functools.partial(handle.read, CHUNKSIZE)
    for i, chunk in enumerate(iter(read_chunk, b'')):
        print('{:5d} {!r}'.format(i + 1, chunk))
