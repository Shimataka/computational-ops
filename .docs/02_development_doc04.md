# Implement of Result type

## 実装

```python
from typing import Generic, TypeVar, Union, Callable, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
from functools import wraps

T = TypeVar('T')  # 成功時の型
E = TypeVar('E')  # エラー時の型
R = TypeVar('R')  # 戻り値の型

class Result(Generic[T, E], ABC):
    """RustライクなResult型の基底クラス。

    成功または失敗を表現する型。Rustの Result 型を模倣した実装。

    Attributes:
        T: 成功時の値の型パラメータ
        E: エラー時の値の型パラメータ

    Note:
        全てのメソッドは抽象メソッドとして定義され、Ok または Err クラスで実装される
    """

    @abstractmethod
    def is_ok(self) -> bool:
        """結果が成功かどうかを判定する。

        Returns:
            bool: 成功の場合True、失敗の場合False
        """
        pass

    def is_err(self) -> bool:
        """結果が失敗かどうかを判定する。

        Returns:
            bool: 失敗の場合True、成功の場合False
        """
        return not self.is_ok()

    @abstractmethod
    def unwrap(self) -> T:
        """成功値を取り出す。

        Returns:
            T: 成功時の値

        Raises:
            ValueError: 結果が失敗だった場合
        """
        pass

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        """成功値を取り出すか、失敗時はデフォルト値を返す。

        Args:
            default (T): 失敗時に返すデフォルト値

        Returns:
            T: 成功時は格納された値、失敗時はデフォルト値
        """
        pass

    @abstractmethod
    def unwrap_err(self) -> E:
        """エラー値を取り出す。

        Returns:
            E: エラー値

        Raises:
            ValueError: 結果が成功だった場合
        """
        pass

    @abstractmethod
    def map(self, func: Callable[[T], R]) -> 'Result[R, E]':
        """成功値に関数を適用する。

        Args:
            func (Callable[[T], R]): 適用する関数

        Returns:
            Result[R, E]: 関数適用後の新しいResult
        """
        pass

@dataclass
class Ok(Result[T, E]):
    """成功を表すクラス。

    Attributes:
        value (T): 成功時の値
    """
    value: T

    def is_ok(self) -> bool:
        """結果が成功かどうかを判定する。

        Returns:
            bool: 常にTrue
        """
        return True

    def unwrap(self) -> T:
        """成功値を取り出す。

        Returns:
            T: 格納された値
        """
        return self.value

    def unwrap_or(self, default: T) -> T:
        """成功値を取り出すか、失敗時はデフォルト値を返す。

        Args:
            default (T): 使用されない

        Returns:
            T: 格納された値
        """
        return self.value

    def unwrap_err(self) -> E:
        """エラー値を取り出す。

        Raises:
            ValueError: 常に発生（Okに対して呼び出されるため）
        """
        raise ValueError(f"Called unwrap_err on an Ok value: {self.value}")

    def map(self, func: Callable[[T], R]) -> Result[R, E]:
        """成功値に関数を適用する。

        Args:
            func (Callable[[T], R]): 適用する関数

        Returns:
            Result[R, E]: 関数を適用した結果を含む新しいOk
        """
        return Ok(func(self.value))

@dataclass
class Err(Result[T, E]):
    """エラーを表すクラス。

    Attributes:
        error (E): エラー値
    """
    error: E

    def is_ok(self) -> bool:
        """結果が成功かどうかを判定する。

        Returns:
            bool: 常にFalse
        """
        return False

    def unwrap(self) -> T:
        """成功値を取り出す。

        Raises:
            ValueError: 常に発生（Errに対して呼び出されるため）
        """
        raise ValueError(f"Called unwrap on an Err value: {self.error}")

    def unwrap_or(self, default: T) -> T:
        """成功値を取り出すか、失敗時はデフォルト値を返す。

        Args:
            default (T): 返すデフォルト値

        Returns:
            T: デフォルト値
        """
        return default

    def unwrap_err(self) -> E:
        """エラー値を取り出す。

        Returns:
            E: 格納されたエラー値
        """
        return self.error

    def map(self, func: Callable[[T], R]) -> 'Result[R, E]':
        """成功値に関数を適用する。

        Args:
            func (Callable[[T], R]): 使用されない

        Returns:
            Result[R, E]: 元のエラーを保持した新しいErr
        """
        return Err(self.error)

def result(func: Callable[..., Result]) -> Callable[..., Result]:
    """ハテナ演算子の機能を実現するデコレータ。

    Result型を返す関数内で他のResult型を返す関数を簡潔に扱えるようにする。

    Args:
        func (Callable[..., Result]): デコレートする関数

    Returns:
        Callable[..., Result]: デコレートされた関数

    Note:
        このデコレータは、関数内でquestion関数を使用した際の
        UnwrapErrorを捕捉し、元のErrをそのまま返す。
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Result:
        try:
            return func(*args, **kwargs)
        except UnwrapError as e:
            return e.result
    return wrapper

class UnwrapError(Exception):
    """ハテナ演算子の実装のために使用する例外。

    Attributes:
        result (Result): エラー時のResult
    """
    def __init__(self, result: Result):
        self.result = result

def question(result: Result[T, E]) -> T:
    """ハテナ演算子の機能を実現する関数。

    Ok の場合は値を返し、Err の場合は UnwrapError を送出する。

    Args:
        result (Result[T, E]): 評価するResult

    Returns:
        T: Okの場合の値

    Raises:
        UnwrapError: resultがErrの場合
    """
    if isinstance(result, Ok):
        return result.value
    raise UnwrapError(result)

# エイリアスとしてクエスチョンマークも定義
q = question
```

## 使用例

```python
@result
def divide(a: int, b: int) -> Result[float, str]:
    if b == 0:
        return Err("ゼロ除算エラー")
    return Ok(a / b)

@result
def double_and_add_one(x: float) -> Result[float, str]:
    return Ok(x * 2 + 1)

# ハテナ演算子を使用した例
@result
def complex_calculation(a: int, b: int) -> Result[float, str]:
    # divide の結果が Err の場合、即座に Err を返す
    divided = question(divide(a, b))
    # 成功した場合のみ、この行が実行される
    result = question(double_and_add_one(divided))
    return Ok(result)

# 使用例
result1 = complex_calculation(10, 2)
print(result1)  # Ok(value=11.0)

result2 = complex_calculation(10, 0)
print(result2)  # Err(error='ゼロ除算エラー')

# question のエイリアスとして q を使用する例
@result
def shorter_calculation(a: int, b: int) -> Result[float, str]:
    divided = q(divide(a, b))
    result = q(double_and_add_one(divided))
    return Ok(result)
```
