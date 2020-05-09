from cx_Freeze import *

shortcut_table = [
    ("StartShortcut",        # Shortcut
     "ProgramMenuFolder",          # Directory_
     "CryptoBabble",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]client-chat.exe",  # Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]

# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}

# Change some default MSI options and specify the use of the above defined tables
bdist_msi_options = {'data': msi_data}

setup(
    name = "CryptoBabble",
    version = "1.0",
    description = "An encrypted messaging program.",
    author = "Ed Clark",
    options = {
        "bdist_msi": bdist_msi_options,
        "build_exe":
            {"packages":
                ["cryptography", "socket", "tkinter", "threading", "base64", "hashlib"],
            "include_files":
                ["logo.ico"]
            },
    },
    executables=[Executable("client-chat.pyw", base="Win32GUI", icon="logo.ico")]
)