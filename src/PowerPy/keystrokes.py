# Original PowerCLI script by William Lam - https://github.com/lamw/vmware-scripts/blob/master/powershell/VMKeystrokes.ps1
# Reworked into Python by Tyler Keefe

# TODO: This currently fails when trying to set the LeftShift modifier.
#       Need to figure out how to properly set enum flags in pythonnet.

# TODO: Add support for special key inputs like ENTER, TAB, ESC, etc.

import string
import clr
from logging import getLogger
logger = getLogger(__name__)


# Map subset of USB HID keyboard scancodes
# https://gist.github.com/MightyPork/6da26e382a7ad91b5496ee55fdc73db2
hidCharacterMap = {
    "a"            : 0x04,
    "b"            : 0x05,
    "c"            : 0x06,
    "d"            : 0x07,
    "e"            : 0x08,
    "f"            : 0x09,
    "g"            : 0x0a,
    "h"            : 0x0b,
    "i"            : 0x0c,
    "j"            : 0x0d,
    "k"            : 0x0e,
    "l"            : 0x0f,
    "m"            : 0x10,
    "n"            : 0x11,
    "o"            : 0x12,
    "p"            : 0x13,
    "q"            : 0x14,
    "r"            : 0x15,
    "s"            : 0x16,
    "t"            : 0x17,
    "u"            : 0x18,
    "v"            : 0x19,
    "w"            : 0x1a,
    "x"            : 0x1b,
    "y"            : 0x1c,
    "z"            : 0x1d,
    "1"            : 0x1e,
    "2"            : 0x1f,
    "3"            : 0x20,
    "4"            : 0x21,
    "5"            : 0x22,
    "6"            : 0x23,
    "7"            : 0x24,
    "8"            : 0x25,
    "9"            : 0x26,
    "0"            : 0x27,
    "!"            : 0x1e,
    "@"            : 0x1f,
    "#"            : 0x20,
    "$"            : 0x21,
    "%"            : 0x22,
    "^"            : 0x23,
    "&"            : 0x24,
    "*"            : 0x25,
    "("            : 0x26,
    ")"            : 0x27,
    "_"            : 0x2d,
    "+"            : 0x2e,
    "{"            : 0x2f,
    "}"            : 0x30,
    "|"            : 0x31,
    ":"            : 0x33,
    "`"           : 0x34,
    "~"            : 0x35,
    "<"            : 0x36,
    ">"            : 0x37,
    "?"            : 0x38,
    "-"            : 0x2d,
    "="            : 0x2e,
    "["            : 0x2f,
    "]"            : 0x30,
    "\\"           : 0x31,
    "`;"           : 0x33,
    "`'"           : 0x34,
    ","            : 0x36,
    "."            : 0x37,
    "/"            : 0x38,
    " "            : 0x2c,
    "F1"           : 0x3a,
    "F2"           : 0x3b,
    "F3"           : 0x3c,
    "F4"           : 0x3d,
    "F5"           : 0x3e,
    "F6"           : 0x3f,
    "F7"           : 0x40,
    "F8"           : 0x41,
    "F9"           : 0x42,
    "F10"          : 0x43,
    "F11"          : 0x44,
    "F12"          : 0x45,
    "TAB"          : 0x2b,
    "KeyUp"        : 0x52,
    "KeyDown"      : 0x51,
    "KeyLeft"      : 0x50,
    "KeyRight"     : 0x4f,
    "KeyESC"       : 0x29,
    "KeyBackSpace" : 0x2a,
    "KeyEnter"     : 0x28,
}

special_chars = string.punctuation + string.ascii_uppercase
            
def _init_vmware_vim(cli):
    # Sometimes, the VMware.Vim module cannot be imported, as it is not available in 
    # the environment. If the CLI object has not yet initialized the VMware.Vim assembly, than
    # self.vmware_vim_initialized will be False. 
    # Running a command that uses VMware.Vim types will cause the assembly to be loaded, even the
    # command itself fails. 
    
    # This will fail, but will load the assembly. 
    try:
        cli.Get_PowerCLIVersion()
    except Exception as e:
        pass

    # We should now be able to load the assembly.
    try:
        clr.AddReference("VMware.Vim")
    except Exception as e:
        print(f"Error loading VMware.Vim: {e}")
        return

    cli.vmware_vim_initialized = True


def type_command(cli, vm, command, newline=True):
    """Types a command into the VM's console.
    args:
        cli: PowerPy CLI instance
        vm: VM object of type 'UniversalVirtualMachineImpl'
        command: string command to type into the VM console
    """
    
    if not cli.vmware_vim_initialized:
        _init_vmware_vim(cli)
    
    # TODO: Enforce vm type check
    # if type(vm) != "UniversalVirtualMachineImpl":
    #     raise TypeError("vm parameter must be of type 'UniversalVirtualMachineImpl'. Use raw=True when retrieving the VM.")

    # TODO: vm_view should return a single object, not a list. Correct this in CLI.py _run method.
    vm_view = cli.Get_View(viobject=vm, raw=True)
    if type(vm_view) == list:
        vm_view = vm_view[0]
    

    from VMware.Vim import UsbScanCodeSpecKeyEvent, UsbScanCodeSpecModifierType, UsbScanCodeSpec
    
    keystrokes = []
    for char in command:
        key_press = UsbScanCodeSpecKeyEvent()
        
        if char in special_chars:
            modifier = UsbScanCodeSpecModifierType
            modifier.LeftShift = True # FIXME: This returns "TypeError: invalid target".
            key_press.Modifiers = modifier
            
        # Convert hex value to HID code format
        hex_code = hidCharacterMap.get(char)
        if hex_code is None:
            raise ValueError(f"Character '{char}' not supported for keystroke injection.")
        
        hex_code = (hex_code << 16) | 0x07
        key_press.UsbHidCode = hex_code
        keystrokes.append(key_press)
        
    if newline:
        key_press = UsbScanCodeSpecKeyEvent()
        key_press.UsbHidCode = (0x28 << 16) | 0x07
        keystrokes.append(key_press)

    spec = UsbScanCodeSpec()
    spec.KeyEvents = keystrokes
    print(f"VM Name: {vm.Name} - Injecting keystrokes for command: {command}")
    try:
        vm.PutUsbScanCodes(spec)
    except Exception as e:
        if "does not implement: PutUsbScanCodes" in str(e):
            logger.warning("vCSim does not support keyboard injection, skipping.")
        else:
            raise
