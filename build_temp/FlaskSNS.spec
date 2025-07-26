# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['..\\FlaskSNS.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\HMYU\\Documents\\CodeSpace\\flask_sns_app\\templates', 'templates'), ('C:\\Users\\HMYU\\Documents\\CodeSpace\\flask_sns_app\\utils', 'utils')],
    hiddenimports=['flask', 'flask_sqlalchemy', 'flask_login', 'werkzeug', 'jinja2', 'sqlalchemy', 'requests', 'bs4', 'PIL', 'filetype'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FlaskSNS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
