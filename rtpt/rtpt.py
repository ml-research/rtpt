"""
RTPT class to rename your processes giving information on who is launching the
process, and the remaining time for it.
Created to be used with our AIML IRON table.
"""
from time import time
from setproctitle import setproctitle

from collections import deque


class RTPT:
    def __init__(
        self,
        name_initials: str,
        experiment_name: str,
        max_iterations: int,
        iteration_start: int = 0,
        moving_avg_window_size: int = 20,
        update_interval: int = 1,
        precision: int = 2,
        no_iterations: bool = False
    ):
        """
        Initialize the Remaining-Time-To-Process (RTPT) object.

        Args:
            name_initials (str): Name initials (e.g. "QD" for "Quentin Delfosse").
            experiment_name (str): A unique name to identify the running experiment.
                Spaces will be replaced with underscores.
            max_iterations (int): The maximum number of iterations.
            iteration_start (int): The iteration at which to start (optional, default: 0).
            moving_avg_window_size (int): The window size for the moving average for the ETA approximation (optional, default: 20).
            update_interval (int): After how many iterations the title should be updated (optional, default: 1).
            precision (int): The Precision of the reported time (optional, default: 2).
            no_iterations (bool): If set to true no ETA will be displayed. The value of `max_iterations` will have no effect if this is set to true.
        """
        # Some assertions upfront
        assert (
            max_iterations > 0
        ), f"Maximum number of iterations has to be greater than 0 but was {max_iterations}"
        assert (
            iteration_start >= 0
        ), f"Starting iteration count must be equal or greater than 0 but was {iteration_start}"

        # Store args
        self.name_initials = name_initials.replace(" ", "_").replace("/", "_")
        self.experiment_name = experiment_name.replace(" ", "_").replace("/", "_")
        self._current_iteration = iteration_start
        self.max_iterations = max_iterations
        self.update_interval = update_interval
        self.precision = precision
        self.no_iterations = no_iterations

        # Store time for each iterations in a deque
        self.deque = deque(maxlen=moving_avg_window_size)

        # Track end of iterations
        self._last_iteration_time_end = None

        # Variable title part
        self._variable_part = None


        # Perform an initial title update
        self._update_title()


    def start(self):
        """Start the internal iteration timer."""
        self._last_iteration_time_start = time()

    def step(self, subtitle=None):
        """
        Perform an update step:
        - Measure new time for the last epoch
        - Update deque
        - Compute new ETA from deque
        - Set new process title with the latest ETA

        Args:
            subtitle (str): Variable part of the title that can be updated in each step (optional, default: None). If None, it doesn't appear at all.
        """
        if self.no_iterations:
            raise RuntimeError("Called `step()` while `no_iterations` is set to True. If you want to display ETA set `no_iterations` to False.")

        # Update subtitle
        self._variable_part = subtitle

        # Add the time delta of the current iteration to the deque
        time_end = time()
        time_delta = time_end - self._last_iteration_time_start
        self.deque.append(time_delta)

        self._update_title()
        self._current_iteration += 1
        self._last_iteration_time_start = time_end

    def _moving_average_seconds_per_iteration(self):
        """Compute moving average of seconds per iteration."""
        return sum(list(self.deque)) / len(self.deque)

    def _get_eta_str(self):
        """Get the eta string in the format 'Dd:H:M:S'."""
        # TODO: This is currently expected and hardcoded in IRON for the first iteration
        if self._current_iteration == 0 or len(self.deque) == 0:
            return "first_epoch"

        # Get mean seconds per iteration
        avg = self._moving_average_seconds_per_iteration()

        # Compute the ETA based on the remaining number of iterations
        remaining_iterations = self.max_iterations - self._current_iteration
        c = remaining_iterations * avg

        # Compute days/hours/minutes/seconds
        days = round(c // 86400)
        hours = round(c // 3600 % 24)
        minutes = round(c // 60 % 60)
        seconds = round(c % 60)

        eta_str = ""
        reported_units = 0
        for durat, unit in zip([days, hours, minutes, seconds], ['d', 'h', 'm', 's']):
            if durat > 0:
                eta_str += f"{durat:>02d}{unit}:"
                reported_units += 1
            if reported_units == self.precision:
                break
        return eta_str[:-1]  # remove the last colon

    def _get_title(self):
        """Get the full process title. Includes name initials, base name and ETA."""
        # Obtain the ETA
        eta_str = self._get_eta_str()

        # Construct the title
        title = f"@{self.name_initials}_{self.experiment_name}"
        if self._variable_part is not None:
            title += f"_{self._variable_part}"
        if eta_str and not self.no_iterations:
            title += f"#{eta_str}"

        return title

    def _update_title(self):
        """Update the process title."""
        title = self._get_title()

        if self._current_iteration % self.update_interval == 0:
            setproctitle(title)

