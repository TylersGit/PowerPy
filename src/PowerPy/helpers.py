from logging import getLogger
from System.Security import SecureString
from System.Management.Automation import PSCredential

logger = getLogger("PowerPy.helpers")

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

def get_last_stream_record(ps_object, stream_name):
    """Retrieve the last record from a specified PowerShell stream (e.g., Error, Warning)."""
    valid_stream_names = ["Error", "Warning", "Verbose", "Debug", "Information", "Progress"]

    if stream_name not in valid_stream_names:
        raise ValueError(f"Invalid stream name: {stream_name}. Must be one of {valid_stream_names}.")

    stream = getattr(ps_object.Streams, stream_name, None)
    logger.debug(f"Retrieving last record from {stream_name} stream.")
    if stream and stream.Count > 0:
        return psobject_to_python(stream[stream.Count - 1])
    
    
    
def create_pscredential(username, password):
    """Create a PSCredential object from a username and password."""
    secure_password = SecureString()
    for char in password:
        secure_password.AppendChar(char)
    secure_password.MakeReadOnly()
    return PSCredential(username, secure_password)