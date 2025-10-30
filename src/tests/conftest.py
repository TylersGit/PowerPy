import os
import pytest
from PowerPy.CLI import CLI

@pytest.fixture(scope="session")
def cli():
    cli = CLI()
    cli.Connect_VIServer(server=os.getenv("VCSIM_SERVER", "vcsim"),
                                user=os.getenv("VCSIM_USER", "administrator"),
                                password=os.getenv("VCSIM_PASSWORD", "password"),
                                port=8989,
                                force=True)
    yield cli
    cli.Disconnect_VIServer()