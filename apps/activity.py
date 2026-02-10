class Activity:
    def __init__(
        self,
        title: str,
        category: str,
        location: str,
        date: str,
        time: str
    ):
        if not all([title, category, location, date, time]):
            raise ValueError("All activity fields must be provided.")

        self.title = title
        self.category = category
        self.location = location
        self.date = date
        self.time = time

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "category": self.category,
            "location": self.location,
            "date": self.date,
            "time": self.time
        }

    def summary(self) -> str:
        return f"{self.title} ({self.category}) at {self.location} on {self.date} at {self.time}"
