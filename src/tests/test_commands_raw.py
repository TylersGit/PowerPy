def test_get_vm_raw(cli):
    """Test retrieving VMs with raw=True to get original PowerShell objects."""
    raw_vms = cli.Get_VM(raw=True)
    for raw_vm in raw_vms:
        assert type(raw_vm).__name__ == "UniversalVirtualMachineImpl"
        
def test_create_vm_raw(cli):
    """Test creating a new VM."""
    vm_name = "TestVM-Pytest"
    vm = cli.New_VM(Name=vm_name, ResourcePool=cli.Get_ResourcePool()[0], Datastore=cli.Get_Datastore(), NumCPU=1, MemoryMB=4, raw=True)
    assert type(vm) == "PSObject"
    assert type(vm).__name__ == "UniversalVirtualMachineImpl"
    assert vm.Name == vm_name
    
def test_get_vm_by_name_raw(cli):
    """Test retrieving a single VM by name."""
    vm_name = "TestVM-Pytest"
    vm = cli.Get_VM(Name=vm_name)
    assert vm.Name == vm_name

    
def test_delete_vm(cli):
    """Test deleting a VM."""
    vm_name = "TestVM-Pytest"
    vm = cli.Get_VM(Name=vm_name)
    cli.Remove_VM(vm, DeletePermanently=True)
    vms_after = cli.Get_VM(Name=vm_name)
    assert vms_after is None