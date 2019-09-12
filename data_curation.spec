# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['data_curation.py'],
             pathex=['/Users/Andres/Desktop/FLIR-Data-Curator-MAC-master-2'],
             binaries=[],
             datas=[],
             hiddenimports=['numpy', 'imagecodecs._imagecodecs_lite', 'tornado'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='data_curation',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='flam.ico')
app = BUNDLE(exe,
             name='data_curation.app',
             icon='flam.ico',
             bundle_identifier=None)
