import time
from functools import wraps


class Timer:
    def __init__(self, label="", verbose=True, force_ms=False, parent=None):
        self.verbose = verbose
        self.label = label
        self.force_ms = force_ms
        self.parent = parent
        self.level = 0
        self.start_time = -1
        self.end_time = -1
        self.report = ""

        if parent:
            self.level = parent.level + 1

    @property
    def root(self):
        root = self
        while root.parent is not None:
            root = root.parent
        return root

    @property
    def total(self):
        return format_time(self.total_time, force_ms=self.force_ms)

    @property
    def total_in_ms(self):
        return format_ms(self.total_time)

    @property
    def total_in_mins(self):
        return format_mins(self.total_time)

    def __enter__(self):
        self.start_time = time.perf_counter()

        if self.verbose:
            self.print("{} start".format(self.label))

        return self

    def __exit__(self, *exc):
        self.end_time = time.perf_counter()
        self.total_time = self.end_time - self.start_time
        if self.verbose:
            self.print("{} end ({})".format(self.label, self.total))

    def __call__(self, func):
        if not self.label:
            self.label = func.__name__

        @wraps(func)
        def inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return inner

    def __repr__(self):
        parent = self.parent.label if self.parent else None
        return "<{}(label={!r}, parent={!r})>".format(type(self).__name__, self.label, parent)

    def print(self, *args):
        now = format_mins(time.perf_counter() - self.root.start_time)
        prefix = "[{}]".format(now)
        prefix = "{:<10}".format(prefix)
        indent = "     " * self.level

        if not indent:
            vals = (prefix, *args)
        else:
            indent = indent[:-2] + "↳ "
            vals = (prefix, indent, *args)

        output = " ".join(vals)
        # FIXME: make this to work properly with parent/child
        self.report += output + "\n"
        if self.root is not self:
            self.root.report += output + "\n"

        if self.verbose:
            print(output)

    def child(self, *args, **kwargs):
        return Timer(*args, parent=self, **kwargs)


def format_time(seconds, force_ms=False):
    if seconds < 1 or force_ms:
        return format_ms(seconds)
    return format_mins(seconds)


def format_ms(seconds):
    return "{:.0f}ms".format(seconds * 1000)


def format_mins(seconds):
    mins, secs = divmod(round(seconds), 60)
    return "{}m{:02.0f}s".format(mins, secs)
