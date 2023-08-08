from datetime import date


class Note(object):
    def __init(self, note_id: int, title: str, text: str, save_date: date):
        self.__note_id = note_id
        self.title = title
        self.text = text
        self.save_date = save_date

    @property
    def id(self) -> int:
        return self.__note_id

    @property
    def title(self) -> str:
        return self.title

    @property
    def text(self) -> str:
        return self.text

    @title.setter
    def title(self, value: str):
        self.title = value

    @text.setter
    def text(self, value: str):
        self.text = value

    @property
    def save_date(self) -> date:
        return self.save_date

    @save_date.setter
    def save_date(self, value: date):
        self.save_date = value
