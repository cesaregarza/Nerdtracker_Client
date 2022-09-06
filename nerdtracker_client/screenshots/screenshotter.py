import time
from threading import Timer
from types import TracebackType

import mss
import numpy as np
import numpy.typing as npt
from mss.screenshot import ScreenShot


class Screenshotter:
    def __init__(
        self,
        monitor_index: int = 1,
        time_interval: int | float = 0.5,
        start_immediately: bool = False,
    ) -> None:
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[monitor_index]
        self.size = (self.monitor["width"], self.monitor["height"])
        self.shape = (self.monitor["height"], self.monitor["width"], 3)
        self.time_interval = float(time_interval)
        self._timer: Timer | None = None
        self._is_running: bool = False
        self.next_call = time.time()
        if start_immediately:
            self.timer_start()

    def _run(self) -> None:
        self._is_running = False
        self.timer_start()
        self.process_screenshot()

    def timer_start(self) -> None:
        if not self._is_running:
            self.next_call += self.time_interval
            self._timer = Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self._is_running = True

    def timer_stop(self) -> None:
        if self._timer is not None:
            self._timer.cancel()
        self._is_running = False

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Upon closing, close mss.mss()

        Args:
            exc_type (type[BaseException] | None): Exception type, unused
            exc_value (BaseException | None): Exception value, unused
            traceback (TracebackType | None): Traceback, unused
        """
        self.sct.close()
        self.timer_stop()

    def take_screenshot(self) -> npt.NDArray[np.uint8]:
        grab = self.sct.grab(self.monitor)
        frame = np.array(grab)
        # Remove the alpha channel, which is always 255
        cut_frame = frame[:, :, :-1]
        return cut_frame

    def process_screenshot(self) -> None:
        screenshot = self.take_screenshot()
