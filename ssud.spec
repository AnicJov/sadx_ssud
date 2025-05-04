# ssud.spec

from PyInstaller.utils.hooks import collect_data_files
from pathlib import Path
import os

block_cipher = None

# Include all files in the res/ folder
res_path = Path('res')
res_datas = [(str(f), str(f.parent)) for f in res_path.rglob('*') if f.is_file()]

a = Analysis(
    ['src/main.py'],
    pathex=['.'],
    binaries=[],
    datas=res_datas,
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ssud',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
