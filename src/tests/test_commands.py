def test_get_vm(cli):
    """Test retrieving VMs and their properties, returning the simpler Python objects."""
    vms = cli.Get_VM()
    for vm in vms:
        assert hasattr(vm, "Name")
        assert hasattr(vm, "PowerState")
        assert repr(vm) == f"<UniversalVirtualMachineImpl Name={vm.Name}>"

def test_get_datastore(cli):
    """Test retrieving Datastores."""
    datastores = cli.Get_Datastore()
    for datastore in datastores:
        assert repr(datastore) == f"<DatastoreImpl Name={datastore.Name}>"
                
def test_create_vm(cli):
    """Test creating a new VM."""
    vm_name = "TestVM-Pytest"
    vm = cli.New_VM(Name=vm_name, ResourcePool=cli.Get_ResourcePool()[0], Datastore=cli.Get_Datastore(), NumCPU=1, MemoryMB=4,)
    assert vm.Name == vm_name
    
def test_get_vm_by_name(cli):
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