import logging
import clr

logger = logging.getLogger("PowerPy.PowerCLIWrapper")

dlls = ["System.Management.Automation.dll", "Microsoft.Management.Infrastructure.dll"]
for dll in dlls:
    try:
        clr.AddReference(f"/opt/microsoft/powershell/{dll}")
        logger.debug(f"Loaded {dll} successfully.")
    except:
        logger.error(f"Failed to load {dll}. Ensure PowerShell is installed.")
        raise
        

from System.Management.Automation import PowerShell


class PowerCLIWrapper:
    def __init__(self):
        logger.debug("Creating PowerShell instance.")
        self.ps = PowerShell.Create()
        logger.debug("PowerShell instance created.")
        logger.debug("Importing VMware PowerCLI module.")
        self.ps.AddCommand("Import-Module").AddArgument("VMware.PowerCLI").AddParameter("-Force").Invoke()
        logger.debug("VMware PowerCLI module imported.")
        self.ps.Commands.Clear()

    def _run(self, cmd, *args, **kwargs):
        logger.debug(f"Running command: {cmd} with args: {args} and kwargs: {kwargs}")
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