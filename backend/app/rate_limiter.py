from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone


@dataclass
class AttemptWindow:
    attempts: deque[datetime] = field(default_factory=deque)
    blocked_until: datetime | None = None


class LoginRateLimiter:
    def __init__(
        self,
        max_attempts: int = 5,
        window_minutes: int = 15,
        block_minutes: int = 15,
    ) -> None:
        self.max_attempts = max_attempts
        self.window = timedelta(minutes=window_minutes)
        self.block_duration = timedelta(minutes=block_minutes)
        self._store: dict[str, AttemptWindow] = {}

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def _prune(self, entry: AttemptWindow, now: datetime) -> None:
        while entry.attempts and (now - entry.attempts[0]) > self.window:
            entry.attempts.popleft()
        if entry.blocked_until and now >= entry.blocked_until:
            entry.blocked_until = None

    def is_blocked(self, key: str) -> bool:
        now = self._now()
        entry = self._store.get(key)
        if entry is None:
            return False
        self._prune(entry, now)
        return entry.blocked_until is not None

    def register_failure(self, key: str) -> None:
        now = self._now()
        entry = self._store.setdefault(key, AttemptWindow())
        self._prune(entry, now)
        entry.attempts.append(now)
        if len(entry.attempts) >= self.max_attempts:
            entry.blocked_until = now + self.block_duration

    def reset(self, key: str) -> None:
        self._store.pop(key, None)


login_rate_limiter = LoginRateLimiter()
