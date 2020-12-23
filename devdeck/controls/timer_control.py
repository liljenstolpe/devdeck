import datetime
import os
import threading
from time import sleep

from devdeck_core.controls.deck_control import DeckControl


class TimerControl(DeckControl):

    def __init__(self, key_no, **kwargs):
        self.start_time = None
        self.end_time = None
        self.thread = None
        super().__init__(key_no, **kwargs)

    def initialize(self):
        with self.deck_context() as context:
            context.set_icon(os.path.join(os.path.dirname(__file__), "../../assets", 'stopwatch.png'))

    def pressed(self):
        if self.start_time is None:
            self.start_time = datetime.datetime.now()
            self.thread = threading.Thread(target=self._update_display)
            self.thread.start()
        elif self.end_time is None:
            self.end_time = datetime.datetime.now()
            self.thread.join()
            with self.deck_context() as context:
                context.render_text(TimerControl.time_diff_to_str(self.end_time - self.start_time),
                                    font_size=120, fill='red')
        else:
            self.start_time = None
            self.end_time = None
            with self.deck_context() as context:
                context.set_icon(os.path.join(os.path.dirname(__file__), "../../assets", 'stopwatch.png'))

    def _update_display(self):
        while self.end_time is None:
            if self.start_time is None:
                sleep(1)
                continue
            cutoff = datetime.datetime.now() if self.end_time is None else self.end_time
            with self.deck_context() as context:
                context.render_text(TimerControl.time_diff_to_str(cutoff - self.start_time), font_size=120)
            sleep(1)

    @staticmethod
    def time_diff_to_str(diff):
        seconds = diff.total_seconds()
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'
