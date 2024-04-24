"""Test the get_deg_min_sec method."""

from sio_postdoc.engine.transformation.strategies.base import TransformationStrategy

ZERO = (1, 0, 0, 0)
POSITIVE = (1, 124, 5, 40)
ONE_EIGHTY = (1, 180, 0, 0)
NEGATIVE = (-1, 135, 54, 20)


def test_negative_900():
    assert TransformationStrategy.get_deg_min_sec(-900) == ONE_EIGHTY


def test_negative_angle_between_neg_720_and_neg_900():
    assert TransformationStrategy.get_deg_min_sec(-720 - 135.9055) == NEGATIVE


def test_negative_720():
    assert TransformationStrategy.get_deg_min_sec(-720) == ZERO


def test_negative_angle_between_neg_540_and_neg_720():
    assert TransformationStrategy.get_deg_min_sec(-360 - 235.9055) == POSITIVE


def test_negative_540():
    assert TransformationStrategy.get_deg_min_sec(-540) == ONE_EIGHTY


def test_negative_angle_between_neg_360_and_neg_540():
    assert TransformationStrategy.get_deg_min_sec(-360 - 135.9055) == NEGATIVE


def test_negative_360():
    assert TransformationStrategy.get_deg_min_sec(-360) == ZERO


def test_negative_angle_between_neg_180_and_neg_360():
    assert TransformationStrategy.get_deg_min_sec(-235.9055) == POSITIVE


def test_negative_180():
    assert TransformationStrategy.get_deg_min_sec(-180) == ONE_EIGHTY


def test_negative_angle_between_0_and_neg_180():
    assert TransformationStrategy.get_deg_min_sec(-135.9055) == NEGATIVE


def test_0():
    assert TransformationStrategy.get_deg_min_sec(0) == ZERO


def test_positive_angle_less_thanONE_EIGHTY():
    assert TransformationStrategy.get_deg_min_sec(124.0945) == POSITIVE


def testONE_EIGHTY():
    assert TransformationStrategy.get_deg_min_sec(180) == ONE_EIGHTY


def test_positive_angle_greater_thanONE_EIGHTY():
    assert TransformationStrategy.get_deg_min_sec(224.0945) == NEGATIVE


def test_360():
    assert TransformationStrategy.get_deg_min_sec(360) == ZERO


def test_positve_angle_between_360_and_540():
    assert TransformationStrategy.get_deg_min_sec(360 + 124.0945) == POSITIVE


def test_540():
    assert TransformationStrategy.get_deg_min_sec(360 + 180) == ONE_EIGHTY


def test_positve_angle_between_540_and_720():
    assert TransformationStrategy.get_deg_min_sec(360 + 224.0945) == NEGATIVE


def test_720():
    assert TransformationStrategy.get_deg_min_sec(720) == ZERO


def test_positve_angle_between_720_and_900():
    assert TransformationStrategy.get_deg_min_sec(720 + 124.0945) == POSITIVE


def test_900():
    assert TransformationStrategy.get_deg_min_sec(900) == ONE_EIGHTY
