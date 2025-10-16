_class_cache = {}

def psobject_to_python(psobj):
    """Convert a PowerShell PSObject to a Python object with dynamic attributes."""
    global _class_cache
    
    typename = psobj.TypeNames[0] if psobj.TypeNames else "PowerCLIObject"
    classname = typename.split(".")[-1]

    if classname not in _class_cache:
        cls = type(classname, (object,), {})
        def __repr__(self):
            return f"<{classname} Name={getattr(self, 'Name', '?')}>"
        setattr(cls, "__repr__", __repr__)
        _class_cache[classname] = cls
    else:
        cls = _class_cache[classname]

    obj = cls()

    for prop in psobj.Properties:
        try:
            val = prop.Value
        except Exception:
            # skip properties that blow up (lazy-loaded or broken)
            continue
        setattr(obj, prop.Name, val)

    return obj
