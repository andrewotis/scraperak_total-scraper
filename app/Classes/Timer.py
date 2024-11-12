from datetime import datetime

class Timer:
    start_time = None
    end_time = None
    duration = None

    def __init__(self):
        self.start_time = datetime.now()

    def stop(self):
        self.end_time = datetime.now()
        self.duration = self.end_time - self.start_time
        return self.format_duration()

    def format_duration(self):
        hours, remainder = divmod(self.duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        formatted = f"{hours:02}:{minutes:02}:{seconds:02}"
        if formatted[:3] == "00:":
            smaller_formatted = f"{minutes:02}:{seconds:02}"
            return smaller_formatted
        else:
            return formatted
