import threading
from typing import Hashable, Optional, TypeVar, Generic

Value = TypeVar('Value')

class _Node(Generic[Value]):
    """Internal node class for doubly linked list."""
    __slots__ = ('key', 'value', 'prev', 'next')

    def __init__(self, key: Hashable, value: Value) -> None:
        self.key = key
        self.value = value
        self.prev: Optional[_Node] = None
        self.next: Optional[_Node] = None

class LRUCache(Generic[Value]):
    """Thread-safe LRU Cache implementation.

    Args:
        capacity: Maximum number of items the cache can hold. Must be positive.
    """

    __slots__ = ('_capacity', '_cache', '_head', '_tail', '_lock')

    def __init__(self, capacity: int = 128) -> None:
        """Initialize cache with given capacity (default 128)."""
        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        self._capacity = capacity
        self._cache: dict[Hashable, _Node[Value]] = {}
        self._head = _Node(None, None)  # dummy head
        self._tail = _Node(None, None)  # dummy tail
        self._head.next = self._tail
        self._tail.prev = self._head
        self._lock = threading.Lock()

    def get(self, key: Hashable) -> Optional[Value]:
        """Get value for key if exists, else None.

        Args:
            key: The key to look up in the cache.

        Returns:
            The value associated with the key, or None if not found.

        Raises:
            TypeError: If key is unhashable.
        """
        try:
            with self._lock:
                node = self._cache.get(key)
                if node is None:
                    return None

                # Move node to head (most recently used)
                self._move_to_head(node)
                return node.value
        except TypeError as e:
            raise TypeError("Key must be hashable") from e

    def put(self, key: Hashable, value: Value) -> None:
        """Add or update key-value pair in cache.

        Args:
            key: The key to insert or update.
            value: The value to associate with the key.

        Raises:
            TypeError: If key is unhashable.
        """
        try:
            with self._lock:
                # If key exists, update value and move to head
                if key in self._cache:
                    node = self._cache[key]
                    node.value = value
                    self._move_to_head(node)
                    return

                # Create new node
                new_node = _Node(key, value)
                self._cache[key] = new_node
                self._add_to_head(new_node)

                # Evict LRU item if capacity exceeded
                if len(self._cache) > self._capacity:
                    lru_node = self._tail.prev
                    if lru_node:
                        self._remove_node(lru_node)
                        del self._cache[lru_node.key]
        except TypeError as e:
            raise TypeError("Key must be hashable") from e

    def __len__(self) -> int:
        """Return current number of items in cache."""
        with self._lock:
            return len(self._cache)

    def __contains__(self, key: Hashable) -> bool:
        """Check if key exists in cache.

        Args:
            key: The key to check.

        Returns:
            True if key exists, False otherwise.

        Raises:
            TypeError: If key is unhashable.
        """
        try:
            with self._lock:
                return key in self._cache
        except TypeError as e:
            raise TypeError("Key must be hashable") from e

    def clear(self) -> None:
        """Remove all items from cache."""
        with self._lock:
            self._cache.clear()
            self._head.next = self._tail
            self._tail.prev = self._head

    def _add_to_head(self, node: _Node[Value]) -> None:
        """Add node right after dummy head."""
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node

    def _remove_node(self, node: _Node[Value]) -> None:
        """Remove node from linked list."""
        prev_node = node.prev
        next_node = node.next
        if prev_node:
            prev_node.next = next_node
        if next_node:
            next_node.prev = prev_node

    def _move_to_head(self, node: _Node[Value]) -> None:
        """Move node to head position (most recently used)."""
        self._remove_node(node)
        self._add_to_head(node)
