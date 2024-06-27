# Author: Josh Brand
# Date: 27-Jun-2024
# Initial Version GUI Only No backend processing

import PySimpleGUI as sg
import os.path
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

matplotlib.use("TkAgg")

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg



file_list_column = [
    [
        sg.Text("Data Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]
# For now will only show the name of the file that was chosen
data_viewer_column = [
    [sg.Text("Choose an Data Source from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Canvas(key="-CANVAS-")],
]
# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(data_viewer_column),
    ]
]
window = sg.Window("R Wave Detection ", layout, finalize=True)

while True:
    # Add the plot to the window
    draw_figure(window["-CANVAS-"].TKCanvas, fig)
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
        # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            try:
                # Get list of files in folder
                file_list = os.listdir(folder)
            except:
                file_list = []

            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                   and f.lower().endswith((".png", ".gif"))
            ]
            window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            window["-DATA-"].update(filename=filename)
        except:
            pass
window.close()