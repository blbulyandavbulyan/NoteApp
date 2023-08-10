from datetime import datetime


class BaseNote(object):
    def __init__(self, title: str, text: str, save_date: datetime):
        self.title = title
        self.text = text
        self.save_date = save_date

    @property
    def title(self) -> str:
        return self.__title

    @property
    def text(self) -> str:
        return self.__text

    @title.setter
    def title(self, value: str):
        self.__title = value

    @text.setter
    def text(self, value: str):
        self.__text = value

    @property
    def save_date(self) -> datetime:
        return self.__save_date

    @save_date.setter
    def save_date(self, value: datetime):
        self.__save_date = value


class Note(BaseNote):

    def __init__(self, note_id: int, base_note: BaseNote):
        super().__init__(base_note.title, base_note.text, base_note.save_date)
        self.__note_id = note_id

    @property
    def id(self) -> int:
        return self.__note_id
