class RedditPost:
    def __init__(self, text, date, score):
        self.text = text
        self.date = date
        self.score = score

    def __repr__(self):
        return f"[{self.date}] Score: {self.score:.4f} | Text: {self.text}"

