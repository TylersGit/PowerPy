import pytest
from PowerPy.keystrokes import type_command

# TODO: vcsim does not support USB injection, so these tests cannot be fully validated at the moment.
#       In the future, consider mocking the vm.PutUsbScanCodes method to verify correct behavior.

@pytest.fixture()
def vm(cli):
    vm = cli.Get_VM(raw=True)[0]
    yield vm
    cli.Release_VM(vm)

# def test_type_command_basic(cli, vm):
#     type_command(cli, vm, "echo hello")
    
# def test_type_command_no_newline(cli, vm):
#     type_command(cli, vm, "Hello", newline=False)
    
# def test_type_command_special_chars(cli, vm):
#     type_command(cli, vm, "echo !@#$%^&*()_+")
    
# def test_type_command_empty(cli, vm):
#     type_command(cli, vm, "")
    
# def test_type_command_long_string(cli, vm):
#     long_command = "echo " + "A" * 500
#     type_command(cli, vm, long_command)
    
def test_passing_invalid_vm(cli):
    with pytest.raises(TypeError):
        type_command(cli, "NotAValidVMObject", "echo test")