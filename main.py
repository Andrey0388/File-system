global folders, files
folders = []
files = []


class File:
    def __init__(self, name, content, folder):
        self.name = name
        self.content = content
        self.folder = folder
        if folder is not None:
            self.path = folder.path + '/' + self.name
        else:
            self.path = '/' + self.name
        files.append(self)

    def edit_name(self, file_name):
        self.name = file_name

    def edit_content(self, file_content):
        self.content = file_content

    def new_path(self, folder):
        self.path = folder.path + '/' + self.name
        self.folder.data.remove(self)
        self.folder = folder

    def delete(self):
        self.folder.data.remove(self)
        global files
        files.remove(self)


class Folder:
    def __init__(self, name, folder):
        self.folder = folder
        self.name = name
        self.data = []
        if folder is not None:
            self.path = folder.path + '/' + self.name
        else:
            self.path = '/' + self.name
        folders.append(self)

    def append(self, file):
        self.data.append(file)

    def sorted_alphabet(self, reverse):
        self.data.sort(key=lambda x: x.name, reverse=reverse)

    def sorted_length(self, reverse):
        self.data.sort(key=lambda x: len(x.name), reverse=reverse)

    def edit_name(self, file_name):
        self.name = file_name

    def new_path(self, folder):
        self.path = folder.path + '/' + self.name
        self.folder.remove(self.name)
        self.folder = folder

    def delete(self):
        while self.data:
            self.data[0].delete()
        global folders
        folders.remove(self)
        self.folder.data.remove(self)


def move(folder_name, file_name):
    for i in folders:
        if i.name == folder_name:
            folder = i
            break
    else:
        return 1
    for i in files:
        if i.name == file_name:
            file = i
            break
    else:
        return 1

    folder.append(file)

    file.new_path(folder)

    return 0


def search(file_name):
    for i in folders:
        if i.name == file_name:
            return i
    for i in files:
        if i.name == file_name:
            return i
    return None


def menu(key):
    print('Список доступных команд:')
    print('1. Остановить файловую систему')
    print('2. Выйти')
    print('3. Посмотреть содержимое папки или файла')
    print('4. Вернуться назад')
    print('5. Поиск файла по имени')
    if key == 2:
        print('6. Создать новую папку')
        print('7. Создать новый файл')
        print('8. Удалить файл или папку')
        print('9. Переместить файл или папку')
        print('10. Редактировать файл или папку')
        print('11. Сортировать файлы')


def files_conclusion():
    print(f'Текущий путь: {folder.path}')
    print('Список файлов и папок: ')
    if len(folder.data):
        for i in range(len(folder.data)):
            if type(folder.data[i]) == Folder:
                symbol = 'D'
            else:
                symbol = 'F'
            print(f'{i + 1}. [{symbol}] {folder.data[i].name}')
    else:
        print('Здесь файлов нет')


folder = Folder('base', None)

print('Добро пожаловать в файловую систему!')


def main():
    global folder
    print('Варианты входа: ')
    print('1. Гость')
    print('2. Пользователь')
    print()
    while True:
        key = input('Выберите вход (номер входа): ')
        if key == '1' or key == '2':
            key = int(key)
            break
        print('Неверный вариант входа')
    while True:
        print()
        files_conclusion()
        print()
        menu(key)
        print()
        command = input('Введите команду (номер команды): ')
        if command == '3':
            if len(folder.data) == 0:
                print('Файлов и папок для открытия нет!')
                print('Создайте новый файл или папку, чтобы воспользоваться данной функцией.')
                continue
            print()
            files_conclusion()
            print()
            file_number = input('Выберите файл или папку для открытия (0 для возврата): ')
            while True:
                if file_number in [str(i + 1) for i in range(len(folder.data))]:
                    file_number = int(file_number) - 1

                    file = folder.data[file_number]
                    if type(file) == Folder:
                        folder = file
                        print()
                        print(f'Успешно открыта папка {folder.name}.')
                        break
                    else:
                        print()
                        print(f'Содержимое файла {file.name}:')
                        for i in file.content:
                            print(i)
                        break
                elif file_number == '0':
                    break
                print('Введён неверный номер файла или папки!')
                file_number = input('Выберите файл или папку для открытия (0 для возврата): ')
        elif command == '6' and key == 2:
            print()
            folder_name = input('Введите название новой папки: ')
            while True:
                if folder_name in [i.name for i in folders]:
                    print('Папка с таким названием уже существует')
                    folder_name = input('Введите название новой папки: ')
                    continue
                if not folder_name:
                    print('Нельзя создать папку с пустым названием')
                    folder_name = input('Введите название новой папки: ')
                    continue
                break
            folder.append(Folder(folder_name, folder))
            print(f'Успешно создана папка {folder_name}')
        elif command == '7' and key == 2:
            print()
            while True:
                file_name = input('Введите название нового файла: ')
                if file_name in [i.name for i in files] or file_name in [i.name for i in folders]:
                    print('Файл с таким названием уже существует!')
                    continue
                if not file_name:
                    print('Нельзя создать файл с пустым названием')
                    continue
                break
            print('Введите содержимое файла (чтобы закончить ввод, введите пустую строку (enter))')
            file_content = []
            content = input()
            while content:
                file_content.append(content)
                content = input()
            folder.append(File(file_name, file_content, folder))
            print(f'Успешно создан файл {file_name}')
        elif command == '8' and key == 2:
            print()
            files_conclusion()
            print()
            file_number = input('Выберите файл или папку для удаления (0 для возврата): ')
            if file_number in [str(i + 1) for i in range(len(folder.data))]:
                file_number = int(file_number) - 1

                file = folder.data[file_number]
                file.delete()
            elif file_number == '0':
                continue
            else:
                print('Введён неверный номер файла или папки!')
        elif command == '9' and key == 2:
            if len(folder.data) == 0:
                print('Файлов и папок для открытия нет!')
                print('Создайте новый файл или папку, чтобы воспользоваться данной функцией.')
                continue
            print()
            files_conclusion()
            print()
            while True:
                file_number = input('Выберите файл или папку для перемещения (0 для возврата): ')
                if file_number in [str(i + 1) for i in range(len(folder.data))]:
                    file_number = int(file_number) - 1

                    file = folder.data[file_number]

                    folder_name = input(f'Введите название папки, в которую вы хотите переместить файл {file.name}')

                    if move(folder_name, file.name) == 0:
                        print(f'Файла {file.name} успешно перемещён в папку {folder_name}')
                    else:
                        print(f'Папки с названием {folder_name} не существует')
                elif file_number == '0':
                    break
                else:
                    print('Введён неверный номер файла или папки!')
                    continue
                break
        elif command == '10' and key == 2:
            print()
            if len(folder.data) == 0:
                print('Файлов и папок для открытия нет!')
                print('Создайте новый файл или папку, чтобы воспользоваться данной функцией.')
                continue
            files_conclusion()
            print()
            while True:
                file_number = input('Выберите файл для редактирования (0 для возврата): ')
                if file_number in [str(i + 1) for i in range(len(folder.data))]:
                    file_number = int(file_number) - 1
                    file = folder.data[file_number]
                    print()
                    if type(file) == File:
                        file_name = input('Введите новое название файла: ')
                        if file_name in [i.name for i in files] or file_name in [i.name for i in folders]:
                            print('Файл с данным названием уже существует')
                            continue
                        print('Введите новое содержимое файла (чтобы закончить ввод, введите пустую строку (enter))')
                        file_content = []
                        content = input()
                        while content:
                            file_content.append(content)
                            content = input()
                        file.edit_name(file_name)
                        file.edit_content(file_content)
                        print(f'Успешно отредактирован файл {file_name}')
                    else:
                        file_name = input('Введите новое название файла: ')
                        if file_name in [i.name for i in files] or file_name in [i.name for i in folders]:
                            print('Файл с данным названием уже существует')
                            continue
                        file.edit_name(file_name)
                        print(f'Успешно отредактирована папка {file_name}')
                elif file_number == '0':
                    break
                else:
                    print('Введён неверный номер файла или папки!')
                    continue
                break
        elif command == '5':
            while True:
                file_name = input('Введите название файла который вы хотите найти (0 для возврата): ')
                file = search(file_name)
                if file is not None:
                    print(f'Путь к файлу {file.path}')
                    while True:
                        answer = input('Посмотреть содержимое этого файла? (0 - открыть, 1 - нет): ')
                        if answer == '0':
                            if type(file) == Folder:
                                print()
                                folder = file
                                break
                            else:
                                print()
                                print(f'Содержимое файла {file.name}:')
                                for i in file.content:
                                    print(i)
                                break
                        elif answer == '1':
                            break
                        else:
                            print('Некорректный ответ')
                    break
                elif file_name == '0':
                    break
                else:
                    print('Такой файл не найден.')
        elif command == '11' and key == 2:
            print()
            print('Способы сортировки (0 для возврата): ')
            print('1. По алфавиту, по возрастанию')
            print('2. По алфавиту, по убыванию')
            print('3. По длине названия, по возрастанию')
            print('4. По длине названия, по убыванию')
            print()
            while True:
                number = input('Выберите сортировку (номер сортировки): ')
                if number == '1':
                    folder.sorted_alphabet(False)
                elif number == '2':
                    folder.sorted_alphabet(True)
                elif number == '3':
                    folder.sorted_length(False)
                elif number == '4':
                    folder.sorted_length(True)
                elif number == '0':
                    break
                else:
                    print('Введён неверный номер сортировки!')
                    continue

                print(f'Успешно отсортирована папка {folder.name}')
                break
        elif command == '4':
            if folder.folder is not None:
                folder = folder.folder
                print(f'Успешно открыта папка {folder.name}')
            else:
                print('Из корневой папки нельзя вернуться назад')
        elif command == '2':
            main()
            return
        elif command == '1':
            return
        else:
            print('Выбран некорректный номер команды!')


if __name__ == '__main__':
    main()
