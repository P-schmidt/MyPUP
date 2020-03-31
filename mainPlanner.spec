# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_dynamic_libs

block_cipher = None
# options = [('v', None, 'OPTION')]
a = Analysis(['C:/Users/Tidi/Desktop/MyPUP/mainPlanner.py'],
             pathex=['C:\\Users\\Tidi\\Desktop\\MyPUP', 'C:\\Users\\Tidi\\AppData\\Roaming\\Python\\Python37\\site-packages', 'C:\\Users\\Tidi\\AppData\\Local\\Programs\\Python\\Python37\\Lib\site-packages'],
             binaries = [('C:\\Program Files (x86)\\Windows Kits\\10\Redist\\10.0.18362.0\\ucrt\\DLLs', 'VSDLLS')],
             datas=[('data', 'data')],
             hiddenimports=['ortools.constraint_solver.pywrapcp', 'ortools.constraint_solver.pywrapcp', 'ortools.constraint_solver.routing_parameters_pb2'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
        #   options,
          [],
          exclude_binaries=True,
          name='mainPlanner',
          debug='imports',
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , 
          icon='C:\\Users\\Tidi\\Desktop\\MyPUP\\icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='mainPlanner')
