import typing


def fullname(klass):
    module = klass.__module__
    if module == 'builtins':
        return klass.__qualname__  # avoid outputs like 'builtins.str'
    return module + '.' + klass.__qualname__


try:
    import numpy as np
    import numpy.typing as npt

    def is_bare_numpy_array(typ) -> bool:
        """
        Test if the type is `np.ndarray` or `npt.NDArray` without type args.

        >>> import numpy as np
        >>> import numpy.typing as npt
        >>> is_bare_numpy_array(npt.NDArray[np.int64])
        False
        >>> is_bare_numpy_array(npt.NDArray)
        True
        >>> is_bare_numpy_array(np.ndarray)
        True
        """
        return typ in (np.ndarray, npt.NDArray)

    def is_numpy_scalar(typ) -> bool:
        try:
            return issubclass(typ, np.generic)
        except TypeError:
            return False

    def serialize_numpy_scalar(arg) -> str:
        return f"{arg.varname}.item()"

    def deserialize_numpy_scalar(arg):
        return f"{fullname(arg.type)}({arg.data})"

    def is_numpy_array(typ) -> bool:
        try:
            origin = typing.get_origin(typ)
            if origin is not None:
                typ = origin
            return issubclass(typ, np.ndarray)
        except TypeError:
            return False

    def serialize_numpy_array(arg) -> str:
        return f"{arg.varname}.tolist()"

    def deserialize_numpy_array(arg) -> str:
        if is_bare_numpy_array(arg.type):
            return f"numpy.array({arg.data})"

        dtype = fullname(arg[1][0].type)
        return f"numpy.array({arg.data}, dtype={dtype})"

except ImportError:

    def is_numpy_scalar(typ) -> bool:
        return False

    def serialize_numpy_scalar(arg) -> str:
        return ""

    def deserialize_numpy_scalar(arg):
        return ""

    def is_numpy_array(typ) -> bool:
        return False

    def serialize_numpy_array(arg) -> str:
        return ""

    def deserialize_numpy_array(arg) -> str:
        return ""
