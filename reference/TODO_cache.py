import inspect
import uuid
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=None)
def get_cache_path(folder_name: str | None = None) -> Path:
    def generate_uuid() -> str:
        """Generate a UUID based on the file of the caller."""
        # Get the stack frame of the caller
        caller_frame = inspect.stack()[2]
        caller_file = caller_frame.filename
        caller_path = Path(caller_file).resolve()
        return str(uuid.uuid5(uuid.NAMESPACE_URL, str(caller_path)))

    try:
        import platformdirs

        root_cache_dir = platformdirs.user_cache_dir()
    except ImportError:
        root_cache_dir = Path.home() / ".cache"

    if not folder_name:
        folder_name = generate_uuid()

    cache_path = Path(root_cache_dir) / folder_name
    cache_path.mkdir(parents=True, exist_ok=True)

    return cache_path


try:
    from diskcache import Cache

    DISK_CACHE = Cache(get_cache_path())
except ImportError:
    DISK_CACHE = None

try:
    from joblib import Memory

    JOBLIB_MEMORY = Memory(get_cache_path(), verbose=0)
except ImportError:
    JOBLIB_MEMORY = None


@lru_cache(maxsize=None)
def ucache(folder_name: str | None = None, use_sql: bool = False):
    """A decorator for caching function results."""

    if use_sql:

        def decorator(func):
            return DISK_CACHE.memoize()(func)

    elif JOBLIB_MEMORY:
        memory = (
            JOBLIB_MEMORY
            if folder_name is None
            else Memory(get_cache_path(folder_name), verbose=0)
        )

        def decorator(func):
            return memory.cache(func)

    else:

        def decorator(func):
            return lru_cache(maxsize=None)(func)

    return decorator
