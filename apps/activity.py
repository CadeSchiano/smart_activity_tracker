class Activity:
    def __init__(self, title, category, location, time):
        self.title = title
        self.category = category
        self.location = location
        self.time = time

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'category': self.category,
            'location': self.location,
            'time': self.time,
        }

   