import sys
from note_repository import CsvNoteFileRepository, AbstractNoteFileRepository, NoteNotFoundException
from note import BaseNote, Note
if __name__ == '__main__':
    args = sys.argv
    command = ""
    value_needed = False
    command_arg = ""
    command_args: dict[str, str] = {
        'title': '',
        'text': ''
    }
    file_name = "notes.csv"
    notes_repository = CsvNoteFileRepository(file_name)
    for arg in args:
        if arg in ("add", "remove", "update"):
            if command == "":
                command = arg
            else:
                print(f"Вы указали две команды: {command}, {arg}, за одну операцию можно выполнить только одну",
                      file=sys.stderr)
                exit(-2)
        elif arg in ("--title", "--text", "--id"):
            if value_needed:
                print(f"После аргумента {command_arg} ожидалось значение!", file=sys.stderr)
            elif arg not in command_args:
                command_arg = arg.removeprefix("--")
                value_needed = True
            else:
                print(f"Вы уже указывали аргумент {arg}")
                exit(-3)
        elif value_needed:
            command_args[command_arg] = arg
            value_needed = False
    try:
        if command == "add":
            notes_repository.add(BaseNote(command_args['title'], command_args['text']))
        elif command == "remove":
            notes_repository.remove(int(command_args['id']))
        elif command == "update":
            if command_args['text'] != '' or command_args['title']:
                notes_repository.update(int(command_args['id']), command_args['title'], command_args['text'])
            else:
                print("Должны быть указаны значения для --title или --text", file=sys.stderr)
                exit(-5)
    except NoteNotFoundException as e:
        print(str(e), file=sys.stderr)
