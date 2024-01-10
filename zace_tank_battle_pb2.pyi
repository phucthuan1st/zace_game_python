from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Point(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ...) -> None: ...

class Tank(_message.Message):
    __slots__ = ("id", "position", "player_name", "health", "direction")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    PLAYER_NAME_FIELD_NUMBER: _ClassVar[int]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    id: int
    position: Point
    player_name: str
    health: int
    direction: str
    def __init__(self, id: _Optional[int] = ..., position: _Optional[_Union[Point, _Mapping]] = ..., player_name: _Optional[str] = ..., health: _Optional[int] = ..., direction: _Optional[str] = ...) -> None: ...

class Bullet(_message.Message):
    __slots__ = ("position", "direction", "owner_id")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    position: Point
    direction: str
    owner_id: int
    def __init__(self, position: _Optional[_Union[Point, _Mapping]] = ..., direction: _Optional[str] = ..., owner_id: _Optional[int] = ...) -> None: ...

class GameState(_message.Message):
    __slots__ = ("tanks", "bullets", "walls", "scores")
    class ScoresEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: int
        def __init__(self, key: _Optional[int] = ..., value: _Optional[int] = ...) -> None: ...
    TANKS_FIELD_NUMBER: _ClassVar[int]
    BULLETS_FIELD_NUMBER: _ClassVar[int]
    WALLS_FIELD_NUMBER: _ClassVar[int]
    SCORES_FIELD_NUMBER: _ClassVar[int]
    tanks: _containers.RepeatedCompositeFieldContainer[Tank]
    bullets: _containers.RepeatedCompositeFieldContainer[Bullet]
    walls: _containers.RepeatedCompositeFieldContainer[Point]
    scores: _containers.ScalarMap[int, int]
    def __init__(self, tanks: _Optional[_Iterable[_Union[Tank, _Mapping]]] = ..., bullets: _Optional[_Iterable[_Union[Bullet, _Mapping]]] = ..., walls: _Optional[_Iterable[_Union[Point, _Mapping]]] = ..., scores: _Optional[_Mapping[int, int]] = ...) -> None: ...

class PlayerAction(_message.Message):
    __slots__ = ("player_id", "action_type", "direction", "message")
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    ACTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    player_id: int
    action_type: str
    direction: str
    message: str
    def __init__(self, player_id: _Optional[int] = ..., action_type: _Optional[str] = ..., direction: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class MapGrid(_message.Message):
    __slots__ = ("rows",)
    ROWS_FIELD_NUMBER: _ClassVar[int]
    rows: _containers.RepeatedCompositeFieldContainer[Row]
    def __init__(self, rows: _Optional[_Iterable[_Union[Row, _Mapping]]] = ...) -> None: ...

class Row(_message.Message):
    __slots__ = ("cells",)
    CELLS_FIELD_NUMBER: _ClassVar[int]
    cells: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, cells: _Optional[_Iterable[str]] = ...) -> None: ...

class PlayerJoinRequest(_message.Message):
    __slots__ = ("player_name",)
    PLAYER_NAME_FIELD_NUMBER: _ClassVar[int]
    player_name: str
    def __init__(self, player_name: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
