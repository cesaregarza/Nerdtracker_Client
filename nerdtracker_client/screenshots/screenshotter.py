import time
from threading import Timer
from types import TracebackType

import mss
import numpy as np
import numpy.typing as npt
import requests


class Screenshotter:
    """Screenshotter class for taking screenshots of the game continuously, with
    a specified time interval between screenshots. The screenshots are then sent
    to the NerdTracker_Server docker container for processing. This class does
    not do any processing itself, it only takes screenshots and sends them to
    the server. The server will then process the screenshots and send the
    results back to the client.
    """

    def __init__(
        self,
        server_address: str,
        monitor_index: int = 1,
        time_interval: int | float = 0.5,
        start_immediately: bool = False,
        timeout: int | float = 10,
    ) -> None:
        """Constructor for the Screenshotter class

        Args:
            server_address (str): The address of the server to send the
                screenshots to.
            monitor_index (int): The monitor index to take screenshots
                from. Not zero-indexed. Defaults to 1.
            time_interval (int | float): The time interval between
                screenshots. Defaults to 0.5.
            start_immediately (bool): Whether or not to start the
                screenshotting immediately. Defaults to False. If True, the
                screenshotting will start immediately upon instantiation.
            timeout (int | float): The timeout for the requests.post
        """
        self.sct = mss.mss()
        self.server_address = server_address
        self.monitor = self.sct.monitors[monitor_index]
        self.size = (self.monitor["width"], self.monitor["height"])
        self.shape = (self.monitor["height"], self.monitor["width"], 3)
        self.time_interval = float(time_interval)
        self._timer: Timer | None = None
        self._is_running: bool = False
        self.next_call = time.time()
        self.timeout = float(timeout)
        if start_immediately:
            self.timer_start()

    def _run(self) -> None:
        """The function that is called by the timer

        This function is called upon by the timer. This function simply flips
        the _is_running flag to False, restarts the timer, and calls the
        process_screenshot function.
        """
        self._is_running = False
        self.process_screenshot()
        self.timer_start()

    def timer_start(self) -> None:
        """Starts the timer"""
        if not self._is_running:
            self.next_call += self.time_interval
            # In case the processing takes longer than the time interval, this
            # ensures the time left is at least 0
            time_left = max(self.next_call - time.time(), 0.0)
            if time_left == 0.0:
                self.next_call = time.time()
            self._timer = Timer(time_left, self._run)
            self._timer.start()
            self._is_running = True

    def timer_stop(self) -> None:
        """Stops the timer"""
        if self._timer is not None:
            self._timer.cancel()
        self._is_running = False

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Upon closing, close mss.mss() and stop the timer, if it is running.

        Args:
            exc_type (type[BaseException] | None): Exception type, unused
            exc_value (BaseException | None): Exception value, unused
            traceback (TracebackType | None): Traceback, unused
        """
        self.sct.close()
        self.timer_stop()

    def take_screenshot(self) -> npt.NDArray[np.uint8]:
        """Takes a screenshot of the given monitor

        Returns:
            npt.NDArray[np.uint8]: The screenshot as a numpy array, without the
                alpha channel
        """
        grab = self.sct.grab(self.monitor)
        frame = np.array(grab)
        # Remove the alpha channel, which is always 255
        cut_frame = frame[:, :, :-1]
        return cut_frame

    def send_screenshot(
        self, screenshot: npt.NDArray[np.uint8]
    ) -> requests.Response:
        """Sends the screenshot to the server for processing.

        Args:
            screenshot (npt.NDArray[np.uint8]): The screenshot to send to the
                server.

        Returns:
            requests.Response: The response from the server.
        """
        array_string = np.array_str(screenshot)
        response = requests.post(
            self.server_address, data=array_string, timeout=self.timeout
        )
        return response

    def process_screenshot(self) -> None:
        screenshot = self.take_screenshot()
        self.send_screenshot(screenshot)
