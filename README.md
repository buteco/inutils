# inutils

INternational UTILS - random utilities


## Installation

```
pip install inutils
```


## Examples

### Timer

```python
>>> from inutils.timer import Timer
>>> with Timer('task'):
...     time.sleep(1.5)
...
[0m00s]  task start
[0m02s]  task end (0m02s)
>>> @Timer()
... def my_func():
...     time.sleep(3.6)
...
>>> my_func()
[0m00s]  my_func start
[0m04s]  my_func end (0m04s)

```

### Time formatting

```python
>>> from inutils.timer import format_time, format_ms, format_mins
>>> format_mins(1234)  # input time in seconds
'20m34s'
>>> format_ms(0.666)
'666ms'
>>> format_time(0.999)
'999ms'
>>> format_time(1.001)
'0m01s'
```

### Grouping iterables by fixed length

```python
>>> from inutils import chunkify
>>> chunkify([1, 2, 3, 4, 5], chunk_size=2)  # generator
<generator object chunkify at 0x1fa24e625a10>
>>> list(chunkify([1, 2, 3, 4, 5], chunk_size=2))
[[1, 2], [3, 4], [5]]
>>> list(chunkify(['a', 'b', 'c', 'd', 'e'], chunk_size=4))
[['a', 'b', 'c', 'd'], ['e']]
```
