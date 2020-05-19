from itertools import islice


def chunkify(iterable, chunk_size, start=0):
    while (chunk := list(islice(iterable, start, start + chunk_size))) :
        yield chunk
        start += chunk_size
