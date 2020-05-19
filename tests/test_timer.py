import functools
import re
import time
from unittest import mock

from inutils.timer import Timer, format_mins, format_ms, format_time

round2 = functools.partial(round, ndigits=2)

ms_regex = re.compile(r"(\d)\d*ms")


def assert_equal_reports(report, str_report):
    lines = str_report.split("\n")
    clean_report = "\n".join(line.lstrip() for line in lines if line)
    assert ms_regex.sub(r"\1ms", report) == ms_regex.sub(r"\1ms", clean_report)


def test_format_time():
    assert format_time(0.01) == "10ms"
    assert format_time(0.1) == "100ms"
    assert format_time(1) == "0m01s"
    assert format_time(10) == "0m10s"
    assert format_time(10, force_ms=True) == "10000ms"
    assert format_time(3620) == "60m20s"


def test_format_ms():
    assert format_ms(0.000000001) == "0ms"
    assert format_ms(0.1) == "100ms"
    assert format_ms(1.555) == "1555ms"


def test_format_mins():
    assert format_mins(0.00001) == "0m00s"
    assert format_mins(1) == "0m01s"
    assert format_mins(10) == "0m10s"
    assert format_mins(60) == "1m00s"
    assert format_mins(72) == "1m12s"
    assert format_mins(3610) == "60m10s"
    assert format_mins(6031) == "100m31s"
    assert format_mins(59.9) == "1m00s"


def test_timer():
    timer = Timer("name")

    assert repr(timer) == "<Timer(label='name', parent=None)>"
    assert timer.label == "name"
    assert timer.verbose is True
    assert timer.force_ms is False
    assert timer.parent is None
    assert timer.level == 0
    assert timer.start_time == -1
    assert timer.end_time == -1
    assert timer.report == ""
    assert timer.root == timer


def test_timer_as_decorator_no_label():
    @Timer()
    def foo():
        time.sleep(0.01)

    foo()

    timer = foo.__closure__[1].cell_contents
    assert round2(timer.total_time) == 0.01
    assert timer.label == "foo"


def test_timer_as_decorator_with_explicit_label():
    @Timer(label="eita")
    def bar():
        time.sleep(0.01)

    bar()

    timer = bar.__closure__[1].cell_contents
    assert round2(timer.total_time) == 0.01
    assert timer.label == "eita"


def test_timer_basic_usage():
    with Timer("label") as timer:
        time.sleep(0.01)

    assert timer.end_time > timer.start_time > 0
    assert round2(timer.total_time) <= 0.02
    assert timer.end_time - timer.start_time == timer.total_time
    assert timer.total.endswith("ms")
    assert timer.total == timer.total_in_ms
    assert timer.total_in_mins == "0m00s"
    assert_equal_reports(
        timer.report,
        """
        [0m00s]    label start
        [0m00s]    label end (10ms)
    """,
    )


def test_timer_multiple():
    with Timer("1") as timer1:
        time.sleep(0.03)

        with Timer("2") as timer2:
            time.sleep(0.01)

    assert round2(timer2.total_time) == 0.01
    assert round2(timer1.total_time) == 0.04


def test_timer_child_one_level():
    with Timer("parent") as timer:
        time.sleep(0.03)

        with timer.child("child") as child:
            time.sleep(0.01)

    assert round2(child.total_time) == 0.01
    assert child.parent == timer
    assert child.level == 1
    assert_equal_reports(
        child.report,
        """
        [0m00s]       ↳  child start
        [0m00s]       ↳  child end (10ms)
    """,
    )

    assert round2(timer.total_time) == 0.04
    assert_equal_reports(
        timer.report,
        """
        [0m00s]    parent start
        [0m00s]       ↳  child start
        [0m00s]       ↳  child end (10ms)
        [0m00s]    parent end (40ms)
    """,
    )


def test_timer_two_childs():
    with Timer("parent") as timer:
        time.sleep(0.01)

        with timer.child("child1") as child1:
            time.sleep(0.02)

        with timer.child("child2") as child2:
            time.sleep(0.01)

    assert round2(child1.total_time) == 0.02
    assert child1.parent == timer
    assert child1.level == 1
    assert_equal_reports(
        child1.report,
        """
        [0m00s]       ↳  child1 start
        [0m00s]       ↳  child1 end (200ms)
    """,
    )

    assert round2(child2.total_time) == 0.01
    assert child2.parent == timer
    assert child2.level == 1
    assert_equal_reports(
        child2.report,
        """
        [0m00s]       ↳  child2 start
        [0m00s]       ↳  child2 end (100ms)
    """,
    )

    assert round2(timer.total_time) == 0.04
    assert_equal_reports(
        timer.report,
        """
        [0m00s]    parent start
        [0m00s]       ↳  child1 start
        [0m00s]       ↳  child1 end (200ms)
        [0m00s]       ↳  child2 start
        [0m00s]       ↳  child2 end (100ms)
        [0m00s]    parent end (400ms)
    """,
    )


@mock.patch("inutils.timer.time.perf_counter")
def test_report_total_time_more_than_six_chars(counter_mock):
    counter_mock.side_effect = [0, 0, 612, 612]

    with Timer("foo") as timer:
        pass

    assert_equal_reports(
        timer.report,
        """
        [0m00s]    foo start
        [10m12s]   foo end (10m12s)
        """,
    )
