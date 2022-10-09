#!/usr/bin/env python
"""
                     GNU AFFERO GENERAL PUBLIC LICENSE
                       Version 3, 19 November 2007
  Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
  Everyone is permitted to copy and distribute verbatim copies
  of this license document, but changing it is not allowed.
"""
from clr_loader import get_coreclr
from pythonnet import set_runtime
import sys
import platform
import os
from lib.config import config
UVTOOLS_PATH = None
if platform.system() == 'Windows':
    try:
        import winreg

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\UVtools', 0, winreg.KEY_READ)
        UVTOOLS_PATH = winreg.QueryValueEx(key, 'InstallDir')[0]
        if key:
            winreg.CloseKey(key)
    except:
        pass
else:
    UVTOOLS_PATH = config['uvtoolspath']

if UVTOOLS_PATH is None or not os.path.exists(UVTOOLS_PATH):
    print("Unable to find UVtools path, please install and register the path with a Environment Variable (UVTOOLS_PATH)")
    exit(-1)

# Don't touch
# Set runtime
sys.path.append(UVTOOLS_PATH)
rt = get_coreclr()#r"UVtools.runtimeconfig.json"
set_runtime(rt)
import clr

clr.AddReference(r"UVtools.Core")
from UVtools.Core import *
from UVtools.Core.EmguCV import *
from UVtools.Core.Extensions import *
from UVtools.Core.FileFormats import *
from UVtools.Core.GCode import *
from UVtools.Core.Layers import *
from UVtools.Core.Managers import *
from UVtools.Core.MeshFormats import *
from UVtools.Core.Network import *
from UVtools.Core.Objects import *
from UVtools.Core.Operations import *
from UVtools.Core.PixelEditor import *
from UVtools.Core.Printer import *
from UVtools.Core.Scripting import *
from UVtools.Core.Suggestions import *
from UVtools.Core.SystemOS import *
