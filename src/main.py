from PowerPy import PowerCLIWrapper

cli = PowerCLIWrapper()

# Connect
conn = cli.Connect_VIServer("my.vcenter.local", "administrator@vsphere.local", "SuperSecret123!")
print("Connected:", conn[0].Name)

# List all VMs
vms = cli.Get_VM()
for vm in vms:
    print(f"VM: {vm.Name}, State: {vm.PowerState}")

# Get a single VM
vm = cli.Get_VM("MyApp-VM")[0]
print("Found VM:", vm.Name)
