# PowerPy

**PowerPy** is an experimental Python wrapper around [VMware PowerCLI](https://developer.vmware.com/powercli), built with [pythonnet](https://github.com/pythonnet/pythonnet).  
The goal: let you interact with vSphere and other VMware products using Python syntax, instead of stringing together raw PowerShell commands.

> ⚠️ **Note:** This is early work — more of a *proof of concept and roadmap* than a full-featured library. Expect breaking changes and incomplete APIs.

---

## ✨ Vision
- Pythonic functions for common PowerCLI workflows (connect, query VMs, power actions)
- Hide the repetitive `AddCommand` / `AddParameter` boilerplate
- Blend PowerCLI automation seamlessly with other Python libraries
- Eventually publish to PyPI for easy installation

---

## 🚧 Current Status
- Basic scaffolding around `pythonnet` and PowerShell interop
- Prototype for connecting to vCenter and running simple commands
- **Not production ready:** API surface is incomplete, error handling is minimal, and breaking changes are likely

---

## 📦 Installation (for contributors/testers)

**Requirements**
- Python 3.9+
- PowerShell 7+
- PowerCLI installed (`Install-Module VMware.PowerCLI`)

**Clone and install locally**

```bash
git clone https://github.com/yourusername/powerpy.git
cd powerpy
pip install -e .
```

---

## 🖥 Example (prototype)

```python
from powerpy import cli

# Connect to vCenter (prototype API)
cli.connect_vcenter(
    server="my.vcenter.local",
    user="administrator@vsphere.local",
    password="SuperSecret!"
)

# Fetch a list of VMs (early stub, return shape may change)
for vm in cli.get_vm():
    print(vm)
```

> Note: examples are goals for the API; exact function names and return formats may still change.

---

## 📖 Roadmap
- Expand coverage for VM, cluster, datastore, and networking operations
- Improve response objects (structured, typed)
- Add async support for long-running jobs
- Publish package to PyPI
- Write tests and CI workflows

---

## 🤝 Contributing
This is very early stage — contributions, experiments, and feedback are welcome.  
Open issues, propose APIs, or just share how you’d like to use Python with PowerCLI.

