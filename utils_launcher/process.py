import time

import subprocess
import shlex


class SubProcess:
    """Esta clase ejecuta un script en segundo plano

    Attributes
    ----------
    scriptArgs : list
        [Nombre del script, args1, arg2, ..., argn]
    pid : int
        Process identification number
    """
    def __init__(self, script):
        self.scriptArgs = shlex.split(script)
        self.commandArgs = ["python3"]
        self.commandArgs.extend(self.scriptArgs)
        self.pid = None

    def runScript(self):
        self.procHandle = subprocess.Popen(self.commandArgs, 
                                           stdout=subprocess.PIPE, 
                                           stderr=subprocess.DEVNULL)
        
        self.pid = self.procHandle.pid 
        return self.procHandle 
    
    def get_pid(self):
        return self.pid
  
    def isScriptRunning(self):
        return self.procHandle.poll() is None
    
    def stopScript(self):
        self.procHandle.terminate()
        time.sleep(2)

        # Forcefully terminate the script
        if self.isScriptRunning(): self.procHandle.kill()
    
    def getOutput(self):
        # stderr will be redirected to stdout due "stderr=subprocess.STDOUT" 
        # argument in Popen call
        stdout, _ = self.procHandle.communicate()
        returncode = self.procHandle.returncode
        return returncode, stdout