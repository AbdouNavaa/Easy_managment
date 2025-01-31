# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['home.py'],
    pathex=['c:\\Users\\Abdou\\Downloads\\Desktop\\Tkinter-Exemples\\Cars_in_Tkinter\\App'],
    binaries=[],
    datas=[('user_data.json', '.'), ('frames/*.py', 'frames')],
    hiddenimports=['frames','pymysql', 'PIL', 'pandas', 'tkcalendar', 'bcrypt', 'customtkinter'],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='home',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)