from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EmojiToken:
    """Canonical, comparable form of an emoji used for storage and matching.

    Unicode emoji → the character itself ("🎉").
    Custom emoji  → "<:name:id>" or "<a:name:id>".

    Discord's PartialEmoji has the same str() representation in both cases,
    so callers should construct via :meth:`from_string` whether the input came
    from a slash command argument or from str(payload.emoji).
    """

    key: str

    @classmethod
    def from_string(cls, raw: str) -> "EmojiToken":
        token = raw.strip()
        if not token:
            raise ValueError("emoji cannot be empty")
        return cls(key=token)

    def __str__(self) -> str:
        return self.key
