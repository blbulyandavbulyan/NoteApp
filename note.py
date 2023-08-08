from datetime import date


class BaseNote(object):
    def __init(self, title: str, text: str, save_date: date):
        self.title = title
        self.text = text
        self.save_date = save_date

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


class Note(BaseNote):

    def __init__(self, note_id: int, base_note: BaseNote):
        super().__init__(base_note.title, base_note.text, base_note.save_date)
        self.__note_id = note_id

    @property
    def id(self) -> int:
        return self.__note_id
