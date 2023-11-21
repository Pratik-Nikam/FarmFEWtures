import os
import pynetlogo

dirname = os.path.dirname(__file__)
netlogo = None


def get_netlogo_instance():
    global netlogo
    if netlogo is None:
        # jvm_path = "/Library/Java/JavaVirtualMachines/jdk-19.jdk/Contents/MacOS/libjli.dylib"
        netlogo = pynetlogo.NetLogoLink(
            gui=False,
            # jvm_path="/Library/Java/JavaVirtualMachines/jdk-19.jdk/Contents/MacOS/libjli.dylib",
        )
        print(dirname)
        print(
            os.path.join(dirname, "netlogo/FEWCalc_Export_Test.nlogo"),
            "======================",
        )
        netlogo.load_model(os.path.join(dirname, "netlogo/FEWCalc_Export_Test.nlogo"))
        # netlogo.command("setup")
    return netlogo
