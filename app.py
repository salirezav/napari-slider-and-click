import os
from skimage import data, io
import matplotlib.pyplot as plt
import seaborn as sns
import napari
from qtpy.QtWidgets import QSlider
from qtpy.QtCore import Qt
from magicgui import magicgui
from skimage.morphology import binary_dilation, binary_erosion
from scipy import ndimage as ndi
import numpy as np

# loads the image
toxo = io.imread("image.png")
# we need the width and height of the image later
width, height, channels = toxo.shape

# loads the crosshair image to put in place of mouse click
cross = io.imread("crosshair.png")


with napari.gui_qt():
    viewer = napari.Viewer()
    layer = viewer.add_image(toxo)

    # callback function for mouse click
    def my_custom_callback(viewer, value):
        viewer.status = str(value)
        # HERE YOU GET THE VALUE OF THE SLIDER
        # since slider's min-max is 0-1000 we need to divide its value by 1000 to get something between 0-1
        print(value/1000)
    # creating a slider
    my_slider = QSlider(Qt.Horizontal)
    # minimum and maximm values that the slider can have
    my_slider.setMinimum(0)
    my_slider.setMaximum(1000)
    # steps (resolution) of the slider value
    my_slider.setSingleStep(1)
    # here we are binding the callback function to slider's "valueChanged" event
    my_slider.valueChanged[int].connect(
        lambda value=my_slider: my_custom_callback(viewer, value)
    )
    viewer.window.add_dock_widget(my_slider, name='my slider', area='left')

    # appending a mouse_drag callback
    @layer.mouse_drag_callbacks.append
    def get_connected_component_shape(layer, event):
        # we need rounded coordinate values of the mouse click, otherwise it would be a float value instead of integer
        cords = np.round(layer.coordinates).astype(int)
        # here I only intercept the clicks followed by holding the shift key
        if "Shift" in event.modifiers:
            # checking if the click location is outside of image boundaries
            if cords[0] < 0 or cords[1] < 0 or cords[0] > width or cords[1] > height:
                print("outside image dimensions")
                return
            # HERE YOU GET THE COORDINATES OF THE CLICK
            print(cords)

            # some calculations needed to know where to put the crosshair image
            crosscoords = cords
            crosscoords[0] -= 15
            crosscoords[1] -= 15
            # adding the crosshair image to the view
            viewer.add_image(
                cross, name="crosshair", translate=crosscoords)
