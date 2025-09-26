import clr

clr.AddReference("/opt/microsoft/powershell/System.Management.Automation.dll")
clr.AddReference("/opt/microsoft/powershell/Microsoft.Management.Infrastructure.dll")

from System.Management.Automation import PowerShell


class PowerCLIWrapper:
    def __init__(self):
        self.ps = PowerShell.Create()
        self.ps.AddCommand("Import-Module").AddArgument("VMware.PowerCLI").Invoke()
        self.ps.Commands.Clear()

    def _run(self, cmd, *args, **kwargs):
        self.ps.AddCommand(cmd)
        for arg in args:
            self.ps.AddArgument(arg)
        for k, v in kwargs.items():
            self.ps.AddParameter(k, v)
        results = self.ps.Invoke()
        self.ps.Commands.Clear()
        return results


    # Example cmdlet wrappers
    def Connect_VIServer(self, server, user, password):
        return self._run("Connect-VIServer", Server=server, User=user, Password=password)

    def Get_VM(self, name=None):
        if name:
            return self._run("Get-VM", Name=name)
        return self._run("Get-VM")