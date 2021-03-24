# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['game.py'],
             pathex=['C:\\Users\\6thet\\Documents\\GIT-PROJECTS\\Python\\PHC-Minigolf'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += [('Montserrat-Regular.ttf','C:\\Users\\6thet\\Documents\\GIT-PROJECTS\\Python\\PHC-Minigolf\\assets\\fonts\\Montserrat-Regular.ttf','DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='game',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
