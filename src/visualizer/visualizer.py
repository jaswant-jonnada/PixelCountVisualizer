
import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from os.path import splitext


class PixelCountVisualizer:
    def __init__(self, video) -> None:
        """Initializes the class, a video name is given as input"""
        self._filename = video

        self._r_pixel_values = []
        self._g_pixel_values = []
        self._b_pixel_values = []

        fig, ax = plt.subplots(2)
        self._intensity_plot = ax[0]
        self._image_plot = ax[1]

        self._count = 0
        self._frames = []
        plt.subplots_adjust(bottom=0.25)

    def _plot_frame(self) -> None:
        """Plots each frame on the matplotlib widget"""
        t = range(256)
        lw = 3
        alpha = 0.5

        self._image_plot.axes.get_xaxis().set_visible(False)
        self._image_plot.axes.get_yaxis().set_visible(False)

        self._intensity_plot.set_xlim([0, 255])
        self._intensity_plot.set_ylim([0, 20000])

        histogram_r = self._r_pixel_values[0]
        histogram_g = self._g_pixel_values[0]
        histogram_b = self._b_pixel_values[0]

        self._lineR, = self._intensity_plot.plot(
            t, histogram_r, c='r', lw=lw, alpha=alpha)
        self._lineG, = self._intensity_plot.plot(
            t, histogram_g, c='g', lw=lw, alpha=alpha)
        self._lineB, = self._intensity_plot.plot(
            t, histogram_b, c='b', lw=lw, alpha=alpha)

        img = self._frames[0]

        self._im_plot = self._image_plot.imshow(img)

        plt.show()

    def _update(self, frame_num) -> None:
        """Updates the value of the frame, based on the frame number in the graph"""

        frame_num = int(frame_num - 1)
        self._lineR.set_ydata(self._r_pixel_values[frame_num])
        self._lineG.set_ydata(self._g_pixel_values[frame_num])
        self._lineB.set_ydata(self._b_pixel_values[frame_num])

        self._im_plot.set_data(self._frames[frame_num])

    def _process_image(self) -> None:
        img = cv2.imread(self._filename)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        (r, g, b) = cv2.split(img)

        histogram_r = cv2.calcHist([r], [0], None, [256], [0, 255])
        histogram_g = cv2.calcHist([g], [0], None, [256], [0, 255])
        histogram_b = cv2.calcHist([b], [0], None, [256], [0, 255])

        t = range(256)
        lw = 3
        alpha = 0.5

        self._image_plot.axes.get_xaxis().set_visible(False)
        self._image_plot.axes.get_yaxis().set_visible(False)

        self._intensity_plot.set_xlim([0, 255])
        self._intensity_plot.set_ylim([0, 5000])

        lineR, = self._intensity_plot.plot(
            t, histogram_r, c='r', lw=lw, alpha=alpha)
        lineG, = self._intensity_plot.plot(
            t, histogram_g, c='g', lw=lw, alpha=alpha)
        lineB, = self._intensity_plot.plot(
            t, histogram_b, c='b', lw=lw, alpha=alpha)

        im_plot = self._image_plot.imshow(img)

        plt.show()

    def _process_video(self) -> None:
        capture = cv2.VideoCapture(self._filename)

        while True:
            (grabbed, frame) = capture.read()

            if not grabbed:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            (r, g, b) = cv2.split(frame)

            histogram_r = cv2.calcHist([r], [0], None, [256], [0, 255])
            histogram_g = cv2.calcHist([g], [0], None, [256], [0, 255])
            histogram_b = cv2.calcHist([b], [0], None, [256], [0, 255])

            self._frames.append(frame)

            self._r_pixel_values.append(histogram_r)
            self._g_pixel_values.append(histogram_g)
            self._b_pixel_values.append(histogram_b)

            self._count += 1

        pixel_axis = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor="White")
        self._pixel_slider = Slider(pixel_axis, 'Frame',
                                    0, self._count, valinit=0)
        self._pixel_slider.on_changed(self._update)
        self._plot_frame()

    def run(self) -> None:
        """Public. Should be used to run the plot, once the object is shown"""

        _, file_ext = splitext(self._filename)

        if (file_ext == '.jpg') or (file_ext == '.jpeg'):
            self._process_image()
        elif (file_ext == '.mp4') or (file_ext == '.mov'):
            self._process_video()
        else:
            raise TypeError("Only jpeg and mp4, mov are supported")
