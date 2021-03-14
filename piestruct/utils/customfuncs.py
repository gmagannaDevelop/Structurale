def udir(obj):
    """
    udir : user-dir

    Filters all magic methods and private attributes from a dir() call
    """
    return [attribute for attribute in dir(obj) if "__" not in attribute]
