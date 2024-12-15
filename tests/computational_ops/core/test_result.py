import unittest

from computational_ops.core.result import Err, Ok, Result, question, result


def get_ok_none() -> Result[None, str]:
    return Ok(None)


def get_ok_int() -> Result[int, str]:
    return Ok(1)


def get_err_str() -> Result[None, str]:
    return Err("error")


def get_err_int() -> Result[int, int]:
    return Err(1)


def get_err_valueerror() -> Result[None, ValueError]:
    msg = "error"
    return Err(ValueError(msg))


@result
def get_decorator_int() -> Result[int, str]:
    return Ok(question(get_ok_int()))


@result
def get_decorator_err_int() -> Result[None, int]:
    question(get_err_int())
    return Ok(None)


@result
def get_decorator_valueerr() -> Result[None, ValueError]:
    question(get_err_valueerror())
    return Ok(None)


class TestResult(unittest.TestCase):
    def test_ok(self) -> None:
        assert Ok(1).is_ok()
        assert get_ok_none().unwrap() is None
        assert get_ok_int().unwrap() == 1

    def test_err(self) -> None:
        assert Err("error").is_err()
        assert get_err_str().unwrap_err() == "error"
        assert get_err_int().unwrap_err() == 1
        assert get_err_valueerror().is_err()
        try:
            raise get_err_valueerror().unwrap_err()
        except ValueError as e:
            assert e.args[0] == "error"  # noqa: PT017

    def test_decorator(self) -> None:
        assert get_decorator_int().unwrap() == 1
        assert get_decorator_err_int().is_err()
        assert get_decorator_err_int().unwrap_err() == 1
        assert get_decorator_valueerr().is_err()
        try:
            raise get_decorator_valueerr().unwrap_err()
        except ValueError as e:
            assert e.args[0] == "error"  # noqa: PT017


if __name__ == "__main__":
    unittest.main()
