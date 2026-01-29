class Activity:
    def __init__(self, title: str, category: str, location: str, time: str):
        self.title = title
        self.category = category
        self.location = location
        self.time = time

        if not all([self.title, self.category, self.location, self.time]):
            raise ValueError("All activity fields must be provided.")

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "category": self.category,
            "location": self.location,
            "time": self.time
        }
