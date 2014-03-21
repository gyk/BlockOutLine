from distutils.core import setup
import py2exe
 
includes = ['sip']
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl', 'pyreadline',
            'Tkconstants', 'Tkinter']
packages = []
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                'tk84.dll']

manifest = '''
<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
<assemblyIdentity
version="0.6.8.0"
processorArchitecture="x86"
name="YourApp"
type="win32"
/>
<description>Seequencer</description>
<trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
<security>
<requestedPrivileges>
<requestedExecutionLevel
level="asInvoker"
uiAccess="false"
/>
</requestedPrivileges>
</security>
</trustInfo>
<dependency>
<dependentAssembly>
<assemblyIdentity
type="win32"
name="Microsoft.VC90.CRT"
version="9.0.21022.8"
processorArchitecture="x86"
publicKeyToken="1fc8b3b9a1e18e3b"
/>
</dependentAssembly>
</dependency>
<dependency>
<dependentAssembly>
<assemblyIdentity
type="win32"
name="Microsoft.Windows.Common-Controls"
version="6.0.0.0"
processorArchitecture="x86"
publicKeyToken="6595b64144ccf1df"
language="*"
/>
</dependentAssembly>
</dependency>
</assembly>
''' 

setup(
    version = "0.0.1",
    description = "the 3D Tetris game for flatlanders",
    name = "BlockOutLine",
    options = {"py2exe": {"compressed": 1,
                          "optimize": 2,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 1,
                          "dist_dir": "dist",
                          "xref": False,
                          "skip_archive": False,
                          "ascii": False,
                          "custom_boot_script": '',
                         }
              },
    zipfile = None,
    windows=[{"script":'BlockOutLine.py', 'other_resources' : [(24, 1, manifest)], "icon_resources": [(0, "python.ico")]}]
)