from assertpy import assert_that

from coding_exercise.application.splitter import Splitter
from coding_exercise.domain.model.cable import Cable


def test_should_not_return_none_when_splitting_cable():
    assert_that(Splitter().split(Cable(10, "coconuts"), 1)).is_not_none()


def test_should_raise_error_if_float_provided_for_times():
    splitter = Splitter()
    assert_that(splitter.split).raises(ValueError).when_called_with(
        Cable(1, "coconuts"), 1.6
    )


def test_should_raise_error_if_none_provided_for_times():
    splitter = Splitter()
    assert_that(splitter.split).raises(ValueError).when_called_with(
        Cable(1, "coconuts"), None
    )


def test_should_raise_error_if_negative_provided_for_times():
    splitter = Splitter()
    assert_that(splitter.split).raises(ValueError).when_called_with(
        Cable(1, "coconuts"), -1
    )


def test_should_raise_error_if_times_too_large():
    splitter = Splitter()
    assert_that(splitter.split).raises(ValueError).when_called_with(
        Cable(66, "coconuts"), 65
    )


def test_should_raise_error_if_times_larger_than_length():
    splitter = Splitter()
    assert_that(splitter.split).raises(ValueError).when_called_with(
        Cable(1, "coconuts"), 5
    )


def test_should_raise_error_if_none_provided_for_cable():
    splitter = Splitter()
    assert_that(splitter.split).raises(ValueError).when_called_with(None, 1)


def assert_lengths(cables: list[Cable], lengths: list[int]):
    assert_that(len(cables)).is_equal_to(len(lengths))
    for cable, length in zip(cables, lengths):
        assert_that(cable.length).is_equal_to(length)


def test_correctly_splits_with_no_remainder():
    cables = Splitter().split(Cable(30, "coconuts"), 2)
    assert_lengths(cables, [10, 10, 10])


def test_correctly_splits_with_remainder_into_equal_parts():
    cables = Splitter().split(Cable(5, "coconuts"), 2)
    assert_lengths(cables, [1, 1, 1, 1, 1])


def test_correctly_splits_with_remainder_into_unequal_parts():
    cables = Splitter().split(Cable(10, "coconuts"), 2)
    assert_lengths(cables, [3, 3, 3, 1])


def assert_names_same_length(cables: list[Cable]):
    first_name_len = len(cables[0].name)
    for cable in cables[1:]:
        assert_that(len(cable.name)).is_equal_to(first_name_len)


def test_correctly_pads_names_single_digit():
    cables = Splitter().split(Cable(5, "coconut"), 2)
    assert_names_same_length(cables)
    [first, *_, last] = cables
    assert_that(first.name).is_equal_to("coconut-0")
    assert_that(last.name).is_equal_to("coconut-4")


def test_correctly_pads_names_two_digit():
    cables = Splitter().split(Cable(11, "coconut"), 10)
    assert_names_same_length(cables)
    [first, *_, last] = cables
    assert_that(first.name).is_equal_to("coconut-00")
    assert_that(last.name).is_equal_to("coconut-10")
