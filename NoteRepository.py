from abc import ABC

from note import Note, BaseNote


class AbstractNoteRepository(ABC):
    def __init__(self, notes: list[Note]):
        self.__notes: dict[int, Note] = {}
        self.__next_id: int = notes[0].id
        for note in notes:
            if note.id not in notes:
                self.__notes[note.id] = note
                if note.id > self.__next_id:
                    self.__next_id = note.id
            else:
                raise RuntimeError(f"Дублирующиеся ИД контактов {note.id}")

    def __get_next_id(self) -> int:
        result = self.__next_id
        self.__next_id += 1
        return result

    def add(self, base_note: BaseNote):
        new_id = self.__get_next_id()
        self.__notes[new_id] = Note(new_id, base_note)

    def __getitem__(self, item):
        return self.__notes[item]
