import subprocess
from django.shortcuts import render, redirect
from django.conf import settings
import ast
import numpy as np
import pandas as pd
import types
import plotly.express as px
import matplotlib.pyplot as plt
import json
import os



def ensure_docker_image():
    image_name = "container"
    ruta_proyecto = os.path.join(
            settings.BASE_DIR,
            'simulator',
            'dockers',
            'simulator'
        )
    ruta_docker = os.path.join(ruta_proyecto, image_name)
    resultado = subprocess.run(
            ["docker", "image", "inspect", image_name],
            capture_output=True,
            text=True,
            encoding='utf-8'  
        )
        
    if resultado.returncode != 0:
        try:
            subprocess.run(
            [
            "docker", "build",
            "-f", ruta_docker,
            "-t", image_name,
            ruta_proyecto
            ],
            check=True,
            capture_output=True,
            text=True
            )
        except subprocess.CalledProcessError as e:
            print(e.stdout)
            print(e.stderr)
        
    


def transform_data_numpy(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def revise_value(key,value,dictionary):
        if callable(value):
            return 0
        if value is not None:
            dictionary[key]=value

  



    
