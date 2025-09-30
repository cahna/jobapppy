from typing import IO, Any, Mapping, Optional, Protocol, Sequence, Union

from click.testing import Result


class CliInvoke(Protocol):
    def __call__(
        self,
        args: Union[str, Sequence[str], None] = None,
        input: Union[str, bytes, IO[Any], None] = None,
        env: Optional[Mapping[str, str]] = None,
        catch_exceptions: bool = True,
        color: bool = False,
        **extra: Any,
    ) -> Result: ...
