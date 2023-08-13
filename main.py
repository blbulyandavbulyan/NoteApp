import sys
from note_repository import CsvNoteFileRepository, AbstractNoteFileRepository, NoteNotFoundException
from note import BaseNote
from datetime import datetime

if __name__ == '__main__':
    args = sys.argv
    command = ""
    value_needed = False
    command_arg = ""
    command_args: dict[str, str] = {
        'title': '',
        'text': '',
        'id': '',
        'start-date': '',
        'end-date': ''
    }
    file_name = "notes.csv"
    notes_repository = CsvNoteFileRepository(file_name)
    for arg in args:
        if arg in ("add", "remove", "update", "show"):
            if command == "":
                command = arg
            else:
                print(f"Вы указали две команды: {command}, {arg}, за одну операцию можно выполнить только одну",
                      file=sys.stderr)
                exit(-2)
        elif arg in ("--title", "--text", "--id", "--start-date", "--end-date"):
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
        if command in ("remove", "update", "add"):  # проверка на то, что команда модифицирующая
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
            notes_repository.save()
        elif command == "show":
            if command_args['id'] != '':  # указали ид, значит показываем одну заметку по этому id
                try:
                    note_id = int(command_args['id'])
                    print(notes_repository[note_id])
                except KeyError:
                    print(f"Заметки с заданным ID {command_args['id']} не существует", file=sys.stderr)
            else:  # ид не указали, будем показывать все с учётом фильтров
                filter_date_format = "%m/%d/%y %H:%M"
                start_date: datetime = datetime.strptime(command_args["start-date"], filter_date_format) if command_args["start-date"] != '' else datetime.min
                end_date: datetime = datetime.strptime(command_args["end-date"], filter_date_format) if command_args["end-date"] != '' else datetime.now()
                found_notes = notes_repository.find_all_by(start_date, end_date)
                if len(found_notes) == 0:
                    print("Заметок пока нет")
                for note in found_notes:
                    print(note)
    except NoteNotFoundException as e:
        print(str(e), file=sys.stderr)
