from datetime import datetime


class BaseNote(object):
    def __init__(self, title: str, text: str):
        self.title = title
        self.text = text

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


class Note(BaseNote):

    def __init__(self, note_id: int, save_date: datetime, base_note: BaseNote):
        super().__init__(base_note.title, base_note.text)
        self.__note_id = note_id
        self.__save_date = save_date

    @property
    def id(self) -> int:
        return self.__note_id

    @property
    def save_date(self) -> datetime:
        return self.__save_date
