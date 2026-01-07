"""Unit tests for nt_user_info module."""
from datetime import date

import sys
import pytest

from nt_users_tool.nt_user_info import NTUserInfo, NTUserStatus, evaluate_user_status


def test_python_version():
    """Test the read_nt_users function."""
    # Fail the test if Python version is 3.7
    assert not (sys.version_info.major == 3 and sys.version_info.minor == 7), "This test fails on Python 3.7"


@pytest.mark.parametrize(
    "tests_user_status",
    # day of test : 20/02/2023
    [
        {
            "NTUserStatus": "EXPIRED",
            "expiration_date_year": 2023,
            "expiration_date_month": 1,
            "expiration_date_day": 1,
        },
        {
            "NTUserStatus": "EXPIRING_15_DAYS",
            "expiration_date_year": 2023,
            "expiration_date_month": 2,
            "expiration_date_day": 28,
        },
        {
            "NTUserStatus": "EXPIRING_30_DAYS",
            "expiration_date_year": 2023,
            "expiration_date_month": 3,
            "expiration_date_day": 15,
        },
        {
            "NTUserStatus": "EXPIRING_60_DAYS",
            "expiration_date_year": 2023,
            "expiration_date_month": 4,
            "expiration_date_day": 15,
        },
        {
            "NTUserStatus": "VALID",
            "expiration_date_year": 2024,
            "expiration_date_month": 1,
            "expiration_date_day": 1,
        },
    ],
)
def test_evaluate_expiration_date(mocker, tests_user_status):
    """Test evaluate_user_status function with different expiration dates."""
    # try all kind of expiration status
    mocker.patch("nt_users_tool.nt_user_info._DATE_NOW", date(2023, 2, 20))
    expected_values = getattr(NTUserStatus, tests_user_status["NTUserStatus"])

    test_user = NTUserInfo(
        "",
        "",
        date(
            tests_user_status["expiration_date_year"],
            tests_user_status["expiration_date_month"],
            tests_user_status["expiration_date_day"],
        ),
    )

    test_function_output = evaluate_user_status(test_user)
    assert expected_values == test_function_output


def test_evaluate_expiration_date_invalid_name():
    """Test evaluate_user_status function with invalid name."""
    # try invalid name expiration status
    expected_values = getattr(NTUserStatus, "INVALID_NAME")

    test_user = NTUserInfo("", "", None)

    test_function_output = evaluate_user_status(test_user)
    assert expected_values == test_function_output
