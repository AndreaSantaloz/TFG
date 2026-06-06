import subprocess
import sys
from modulefinder import ModuleFinder
import ast


with open('main.py','r',encoding='utf-8') as f:
    code=f.read()
    tree = ast.parse(code)
    for nodo in ast.walk(tree):
        if isinstance(nodo,ast.Import):
            print(f"Import simple:{[n.name for n in nodo.names]}")
        elif isinstance(nodo,ast.ImportFrom):
            print(f"Import from: {nodo.module}")
            