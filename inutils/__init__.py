import time
from contextlib import ContextDecorator


class Timer(ContextDecorator):
    def __init__(self, label, verbose=True, force_ms=False, parent=None):
        self.children = []
        self.verbose = verbose
        self.label = label
        self.force_ms = force_ms
        self.parent = parent
        self.level = 0

        if parent:
            parent.children.append(self)
            self.level = parent.level + 1

    def __enter__(self):
        self.start = time.perf_counter()

        if self.verbose:
            ellapsed = self.start - self.parent.start if self.parent else 0
            ellapsed = self._format_time(ellapsed)
            self.print("({}) {} start".format(ellapsed, self.label))

        return self

    def __exit__(self, *exc):
        self.total_time = time.perf_counter() - self.start
        if self.verbose:
            self.print("({}) {} end".format(self.total, self.label))

    def print(self, *args):
        indent = "     " * self.level
        if not indent:
            return print(*args)

        indent = indent[:-2] + "↳ "
        print(indent, *args)

    def child(self, *args, **kwargs):
        parent = self if not self.children else self.children[-1]
        kwargs["parent"] = kwargs.get("parent", parent)
        kwargs["level"] = kwargs.get("level", parent.level + 1)
        timer = Timer(*args, **kwargs)
        return timer

    def _format_time(self, seconds):
        if seconds < 1 or self.force_ms:
            return self._format_ms(seconds)
        return self._format_mins(seconds)

    def _format_ms(self, seconds):
        return "{:.0f}ms".format(seconds * 1000)

    def _format_secs(self, seconds):
        mins, secs = divmod(seconds, 60)
        return "{}m{:02.0f}s".format(int(mins), secs)

    @property
    def total(self):
        return self._format_time(self.total_time)

    @property
    def total_in_ms(self):
        return self._format_ms(self.total_time)

    @property
    def total_in_mins(self):
        return self._format_secs(self.total_time)
