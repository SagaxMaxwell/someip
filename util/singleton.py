__all__ = ["singleton"]


def singleton(cls):
    """
    A decorator to implement the Singleton design pattern.

    This decorator ensures that only one instance of the decorated class is created.
    If an instance already exists, the same instance is returned instead of creating a new one.

    Args:
        cls (type): The class to be transformed into a singleton.

    Returns:
        function: A wrapper function that returns the same instance of the class.

    Example:
        >>> @singleton
        ... class Example:
        ...     pass
        >>> a = Example()
        >>> b = Example()
        >>> a is b
        True
    """
    instances = {}

    def get_instance(*args, **kwargs):
        """
        Returns the existing instance of the class or creates a new one if it doesn't exist.

        Args:
            *args: Positional arguments for the class constructor.
            **kwargs: Keyword arguments for the class constructor.

        Returns:
            object: A single instance of the decorated class.
        """
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
