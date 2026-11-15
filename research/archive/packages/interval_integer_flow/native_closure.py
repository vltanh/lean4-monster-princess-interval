"""Discovery-only native flow server; original BigInt verification is retained."""
import json
import os
from pathlib import Path
import subprocess

HERE=Path(__file__).resolve().parent


def compile_helper(directory):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    binary=directory/"integer_maxflow"
    source=HERE/"maximum_flow.cpp"
    if not binary.exists() or binary.stat().st_mtime<source.stat().st_mtime:
        subprocess.run(["g++","-O3","-std=c++17",str(source),"-o",str(binary)],check=True)
    return binary.resolve()


class NativeClosureServer:
    def __init__(self,directory):
        self.binary=compile_helper(directory)
        env=dict(os.environ,PRINCESS_MONSTER_FLOW_BINARY=str(self.binary))
        self.process=subprocess.Popen(["node","--stack-size=16384",str(HERE/"native_server.cjs")],
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1,env=env)

    def ask(self,request):
        self.process.stdin.write(json.dumps(request,separators=(",",":"))+"\n")
        self.process.stdin.flush()
        line=self.process.stdout.readline()
        if not line:raise RuntimeError("native closure server stopped: "+self.process.stderr.read())
        answer=json.loads(line)
        if answer.get("status")=="ERROR":raise RuntimeError(answer["error"])
        return answer

    def close(self):
        if self.process.poll() is None:
            self.ask({"command":"stop"})
            self.process.stdin.close();self.process.wait(timeout=10)
