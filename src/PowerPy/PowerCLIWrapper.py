import logging
import clr

from PowerPy.helpers import psobject_to_python

logger = logging.getLogger("PowerPy.PowerCLIWrapper")

dlls = ["System.Management.Automation.dll", "Microsoft.Management.Infrastructure.dll"]
for dll in dlls:
    try:
        clr.AddReference(f"/opt/microsoft/powershell/{dll}")
        logger.debug(f"Loaded {dll} successfully.")
    except:
        logger.error(f"Failed to load {dll}. Ensure PowerShell is installed.")
        raise
        

from System.Management.Automation import PowerShell, CmdletInvocationException


class PowerCLIWrapper:
    def __init__(self):
        logger.debug("Creating PowerShell instance.")
        self.ps = PowerShell.Create()
        logger.debug("PowerShell instance created.")
        logger.debug("Importing VMware PowerCLI module.")
        # self.ps.AddCommand("Import-Module").AddArgument("VMware.PowerCLI").AddParameter("-Force").Invoke()
        logger.debug("VMware PowerCLI module imported.")
        self.ps.Commands.Clear()

    def _run(self, cmd, *args, **kwargs):
        logger.debug(f"Running command: {cmd} with args: {args} and kwargs: {kwargs}")
        self.ps.AddCommand(cmd)
        for arg in args:
            self.ps.AddArgument(arg)
        for k, v in kwargs.items():
            self.ps.AddParameter(k, v)
        
        
        try:
            results = self.ps.Invoke()
        except CmdletInvocationException as e:
            logger.error(f"Command failed: {e.Message}")
            self.ps.Commands.Clear()
            return None
        self.ps.Commands.Clear()
        return results


    # Example cmdlet wrappers
    def Connect_VIServer(self, server, user, password):
        return self._run("Connect-VIServer", Server=server, User=user, Password=password, WarningAction="SilentlyContinue", Force=True)

    def Get_VM(self, *args, **kwargs):
        result = self._run("Get-VM", *args, **kwargs)
        return [psobject_to_python(obj) for obj in result]