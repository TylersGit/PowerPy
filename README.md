# PowerPy 🐍⚡

A Python wrapper for VMware **PowerCLI** — because I like PowerCLI but dislike PowerShell.  



---

## Overview

PowerPy lets you run PowerCLI commands from Python without fighting PowerShell or multiple Python APIs.  

- All PowerCLI cmdlets are available dynamically after initialization  
- Python-friendly output objects  
- Minimal built-in logging



---

## Installation

Make sure **PowerShell** and **PowerCLI** are installed.

```bash
git clone https://github.com/tylersgit/PowerPy.git
cd PowerPy
pip install -r requirements.txt
```

---

## Usage

```python
from PowerPy.CLI import CLI

cli = CLI()
cli.Connect_VIServer(server="vcenter.local", user="admin", password="secret")

vms = cli.Get_VM()
for vm in vms:
    print(vm.Name)

cli.Disconnect_VIServer()
```

---



## Roadmap
- Send commands directly to console. 
- Better REPL support  
- Publish on PyPI
- Expanded handling for native PowerShell objects (SecureString, PSCredential, etc.)
- Remove the dependancy on Docker. 

---

