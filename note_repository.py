import os.path
from abc import ABC, abstractmethod

from note import Note, BaseNote
import csv
from datetime import datetime


class NoteRepositoryException(RuntimeError):
    pass


class NoteNotFoundException(NoteRepositoryException):
    pass


class DuplicateIdException(NoteRepositoryException):
    pass


class AbstractNoteFileRepository(ABC):
    def __init__(self, file_name: str):
        self._notes: dict[int, Note] = {}
        self.__file_name = file_name
        self._datetime_format = '%m/%d/%y %H:%M:%S'
        self.__saved = False
        self.load(file_name)

    def _parse_list_of_notes(self, notes: list[Note]):
        self.__next_id: int = notes[0].id
        for note in notes:
            if note.id not in notes:
                self._notes[note.id] = note
                if note.id > self.__next_id:
                    self.__next_id = note.id
            else:
                raise DuplicateIdException(f"Дублирующиеся ИД заметок {note.id}")

    def __get_next_id(self) -> int:
        result = self.__next_id
        self.__next_id += 1
        return result

    def add(self, base_note: BaseNote):
        new_id = self.__get_next_id()
        self._notes[new_id] = Note(new_id, datetime.now(), base_note)

    def remove(self, note_id: int):
        if note_id in self._notes:
            self._notes.pop(note_id)
        else:
            raise NoteNotFoundException(f'заметки с id {note_id} нет')

    def update(self, note_id: int, title: str = '', text: str = ''):
        if note_id in self._notes:
            old_note = self._notes[note_id]
            new_note = BaseNote(title if title != '' else old_note.title, text if text != '' else old_note.text)
            self._notes[note_id] = Note(note_id, datetime.now(), new_note)
        else:
            raise NoteNotFoundException(f'заметки с id {note_id} нет')

    def __getitem__(self, item):
        return self._notes[item]

    @property
    def file_name(self):
        return self.__file_name

    @property
    def saved(self):
        return self.__saved

    @abstractmethod
    def load(self, file_name: str):
        self.__file_name = file_name
        self.__saved = True

    @abstractmethod
    def save(self):
        self.__saved = True


class CsvNoteFileRepository(AbstractNoteFileRepository):
    def __init__(self, file_name: str):
        super().__init__(file_name)

    def load(self, file_name: str):
        notes_list: list[Note] = []
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding="UTF-8") as file:
                reader = csv.reader(file)
                for row in reader:
                    notes_list.append(
                        Note(int(row[0]), datetime.strptime(row[1], self._datetime_format), BaseNote(row[2], row[3]))
                    )
            super().load(file_name)
        self._parse_list_of_notes(notes_list)

    def save(self):
        with open(self.file_name, 'w', encoding="UTF-8") as file:
            writer = csv.writer(file)
            for (_, note) in self._notes:
                writer.writerow([note.id, note.save_date, note.title, note.text])
        super().save()
