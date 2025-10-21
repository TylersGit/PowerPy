import logging
from PowerPy.helpers import psobject_to_python

logger = logging.getLogger("PowerPy.CLI")


from System.Management.Automation import PowerShell, CmdletInvocationException


class CLI:
    def __init__(self):
        logger.debug("Creating PowerShell instance.")
        self.ps = PowerShell.Create()
        logger.debug("PowerShell instance created.")
        logger.debug("Importing VMware PowerCLI module.")
        # self.ps.AddCommand("Import-Module").AddArgument("VMware.PowerCLI").AddParameter("-Force").Invoke()
        logger.debug("VMware PowerCLI module imported.")
        self.ps.Commands.Clear()
        self._generate_cmdlets()

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

    def _create_cmdlet_wrapper(self, cmdlet_name):
        def wrapper(*args, **kwargs):
            return self._run(cmdlet_name, *args, **kwargs)
        return wrapper

    def _generate_cmdlets(self):
        cmds = self._run("Get-Command", Module="VMware*")
        for cmd in cmds:
            cmd_py_name = cmd.Name
            cmd_py_name = cmd_py_name.replace("-", "_")
            logger.debug(f"Creating wrapper for cmdlet: {cmd.Name} as method: {cmd_py_name}")
            setattr(self, cmd_py_name, self._create_cmdlet_wrapper(cmd.Name))
            
