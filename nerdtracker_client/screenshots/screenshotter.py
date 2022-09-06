import mss
import numpy as np
import numpy.typing as npt
from mss.screenshot import ScreenShot


class Screenshotter:
    def __init__(self, monitor_index=1) -> None:
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[monitor_index]
        self.size = (self.monitor["width"], self.monitor["height"])
        self.shape = (self.monitor["height"], self.monitor["width"], 3)

    def take_screenshot(self) -> npt.NDArray[np.uint8]:
        grab = self.sct.grab(self.monitor)
        frame = np.array(grab)
        # Remove the alpha channel, which is always 255
        cut_frame = frame[:, :, :-1]
        return cut_frame
