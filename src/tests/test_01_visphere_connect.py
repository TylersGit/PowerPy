import os
import time
import requests
import pytest
from PowerPy.CLI import CLI

requests.packages.urllib3.disable_warnings()

def test_connect_viserver():
    cli = CLI()
    for _ in range(20):
        try:
            res = requests.get("vcsim", verify=False)
            print(f"vCSim HTTP status code: {res.status_code}")
            if res.status_code == 404:
                break
        except:
            print("Waiting for vCSim to be available...")
            time.sleep(1)
            
    
    print("Attempting to connect to vCSim server...")
    print(f"Using server: {os.getenv('VCSIM_SERVER', 'vcsim')}")
    conn = cli.Connect_VIServer(server=os.getenv("VCSIM_SERVER", "vcsim"),
                                user=os.getenv("VCSIM_USER", "administrator"),
                                password=os.getenv("VCSIM_PASSWORD", "password"),
                                port=8989,
                                force=True)
    assert conn.IsConnected 

        
    
    
