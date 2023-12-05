import os
import pynetlogo

dirname = os.path.dirname(__file__)
netlogo = None


def get_netlogo_instance():
    global netlogo
    if netlogo is None:
        jvm_path = "C:\\java\\jdk-12.0.2\\bin\server\\jvm.dll"
        netlogo = pynetlogo.NetLogoLink(
            gui=False,
            jvm_path=jvm_path,
        )
        netlogo.load_model(os.path.join(dirname, "netlogo\\FEWCalc_Export_Test.nlogo"))
        # netlogo.command("setup")
    return netlogo
