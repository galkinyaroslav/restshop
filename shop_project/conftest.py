EVERYTHING_EQUALS_NON_NONE = type('omnieq', (), {'__eq__': lambda x, y: y is not None})()
