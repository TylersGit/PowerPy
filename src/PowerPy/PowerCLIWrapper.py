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
        # Always clear previous commands
        self.ps.Commands.Clear()
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
            return None
        
        if results.Count == 0:
            logger.debug("No results returned from command. Returning None.")
            return None
        
        pythonized_results = [psobject_to_python(obj) for obj in results]
        
        if results.Count == 1:
            logger.debug("Single result returned from command.")
            return pythonized_results[0]
        return pythonized_results


    # Example cmdlet wrappers
    def Connect_VIServer(self, server, user, password):
        return self._run("Connect-VIServer", Server=server, User=user, Password=password, WarningAction="SilentlyContinue", Force=True)

    def Get_VM(self, *args, **kwargs):
        result = self._run("Get-VM", *args, **kwargs)
        return result