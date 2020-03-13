from pathlib import Path

if __name__ == "__main__":
    main()


def main():
    """Stand-alone format converter from v0.2 to v0.1 for 3D printer json control files."""

    import PySimpleGUI as sg

    # Use pysimplegui to open a file browser to get input json file
    layout = [
        [
            sg.Text(
                "Enter json 3D printer control file in version 0.2 format\nto convert to version 0.1 format"
            )
        ],
        [sg.Text("File 1", size=(8, 1)), sg.Input(), sg.FileBrowse()],
        [sg.Submit(), sg.Cancel()],
    ]
    window = sg.Window("Select JSON file", layout)
    event, values = window.read()  # pylint: disable=unused-variable
    window.close()
    print(f"You chose file:\n    {values[0]}")
