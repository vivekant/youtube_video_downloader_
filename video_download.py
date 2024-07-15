import PySimpleGUI as sg
from pytube import YouTube

# Define the layout of the GUI
layout = [
    [sg.Text("Enter YouTube video link:")],
    [sg.InputText(key="-LINK-")],
    [sg.Text("Available qualities:")],
    [sg.Listbox(values=[], key="-QUALITIES-", size=(40, 10))],
    [sg.Button("Get Qualities"), sg.Button("Download")],
    [sg.Text("Destination folder:")],
    [sg.InputText(key="-DESTINATION-"), sg.FolderBrowse()],
]

# Create the GUI window
window = sg.Window("YouTube Video Downloader", layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Get Qualities":
        # Get the video link from the input field
        link = values["-LINK-"]
        try:
            # Create a YouTube object
            yt = YouTube(link)
            # Get the available qualities
            qualities = [f"{s.resolution} - {s.subtype}" for s in yt.streams.filter(only_audio=False)]
            # Update the listbox with the available qualities
            window["-QUALITIES-"].update(values=qualities)
        except Exception as e:
            sg.popup_error(f"Error: e")
    elif event == "Download":
        # Get the selected quality from the listbox
        quality = values["-QUALITIES-"][0]
        # Get the destination folder from the input field
        destination = values["-DESTINATION-"]
        try:
            # Create a YouTube object
            yt = YouTube(link)
            # Filter the streams by the selected quality
            stream = yt.streams.filter(resolution=quality.split(" - ")[0], subtype=quality.split(" - ")[1]).first()
            # Download the video
            stream.download(output_path=destination)
            sg.popup(f"Video downloaded to destination")
        except Exception as e:
            sg.popup_error(f"Error: e")

window.close()