# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Task 1.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/Cinos/AppData/Local/packages/PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0/localcache/local-packages/python311/site-packages/tkinterdnd2', 'tkinterdnd2/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Task 1',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
