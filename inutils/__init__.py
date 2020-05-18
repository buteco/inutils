def chunkify(iterable, chunk_size, start=0):
    while (chunk := iterable[start : start + chunk_size]) :
        yield chunk
        start += chunk_size
