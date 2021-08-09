import json


def open_json() -> dict:
    return json.load(open("data.json", encoding="UTF-8"))


def write_json(js: dict) -> None:
    open("data.json", "w", encoding="UTF-8").write(json.dumps(js))


def add_worker(names: str, date: int) -> None:
    f = open_json()
    f["workers"] += [{
        "date": date,
        "names": names
    }]
    write_json(f)


def get_workers_from_date(date: int) -> list:
    ret = []
    for i in open_json()["workers"]:
        if i["date"] == date:
            ret.append(i["names"])
    return ret


def del_worker(name: str) -> bool:
    f = open_json()

    w = f["workers"]
    for i in range(len(w)):
        if name in w[i]['names']:
            w.pop(i)
            write_json(f)
            return True

    return False


def add_people(people: list) -> None:
    f = open_json()
    f["people"] += people
    write_json(f)


def get_people_count() -> int:
    return len(open_json()["people"])


def get_and_del_first_n_people(n: int) -> list:
    f = open_json()

    ret, f["people"] = f["people"][:n], f["people"][n:]
    write_json(f)
    return ret


def get_works_from_date(date: int, count: int) -> list:

    ret = []
    workers = get_workers_from_date(date)

    if get_people_count() < count * len(workers):
        raise ValueError("Недостаточно людей на проверку.")

    for i in workers:
        ret += [{
            "workers": i,
            "people": get_and_del_first_n_people(count)
        }]

    return ret


def render_work(work: dict) -> str:
    n = '\n'
    return f"Товарищам {work['workers']}\n" \
           f"{n.join(work['people'])}"


def menu_add_worker():
    print("Введите ссылки вк проверяющего и опрашивающего через запятую")
    names = input()
    while not (names and names.isprintable()):
        print("Ошибка")
        print("Введите ссылки вк проверяющего и опрашивающего через запятую")
        names = input()

    print("Введите номер дня недели, когда они будут работать."
          "(1 - пн, 2 - вт...)")
    date = input()
    while not (date and date.isdigit() and 1 <= int(date) <= 7):
        print("Ошибка")
        print("Введите номер дня недели, когда они будут работать."
              "(1 - пн, 2 - вт...)")
        date = input()
    date = int(date)

    add_worker(names, date)
    print("Работники успешно добавлены")


def menu_del_worker():
    print("Введите ссылку вк одного из работников")
    name = input()
    while not (name and name.isprintable()):
        print("Ошибка")
        print("Введите ссылку вк одного из работников")
        name = input()

    if del_worker(name):
        print("Работники успешно удалены")
    else:
        print("Не удалось удалить работников, проверьте введённые данные")


def menu_add_people():
    print("Вводите ссылки вк людей для проверки, каждого с новой строки, в конце нажмите enter")
    p = []
    per = input()
    while per and per.isprintable():
        p += [per]
        per = input()
    add_people(p)
    print("Люди успешно добавлены")


def menu_get_works_from_date():
    print("Введите номер дня недели. (1 - пн, 2 - вт...)")
    date = input()
    while not (date and date.isdigit() and 1 <= int(date) <= 7):
        print("Ошибка")
        print("Введите номер дня недели. (1 - пн, 2 - вт...)")
        date = input()
    date = int(date)

    print("Введите количество людей которые будут назначены каждой группе.")
    count = input()
    while not (count and count.isdigit() and 1 <= int(count)):
        print("Ошибка")
        print("Введите количество людей которые будут назначены каждой группе.")
        count = input()
    count = int(count)

    if get_people_count() < len(get_workers_from_date(date)) * count or get_people_count() == 0:
        print("Недостаточно людей на проверку, уменьшите количество людей на каждую группу")
        return

    print('\n'.join([render_work(i) for i in get_works_from_date(date, count)]))


def menu_get_all_people():
    print("Это действие безвозвратно удалит всех людей на проверку и выведет их на экран.\n"
          "Вы уверены? (Да/нет)")
    if input().lower().strip() == "да":
        print(*get_and_del_first_n_people(get_people_count()), sep='\n')
    else:
        print("Отмена")


def menu_get_all_workers():
    w = []
    for i in open_json()["workers"]:
        w += [i]

    w.sort(key=lambda x: x["date"])

    for i in w:
        print(i["date"])
        print(i["names"])
        print()


if __name__ == '__main__':
    print("Распределитель обязанностей v1")
    print("Выберете необходимое действие")

    funs = (
        menu_add_worker,
        menu_del_worker,
        menu_get_works_from_date,
        menu_add_people,
        menu_get_all_people,
        menu_get_all_workers
    )

    print("1 - Добавить группу работников\n"
          "2 - Удалить группу работников\n"
          "3 - Получить задания для группы работников\n"
          "4 - Добавить людей на проверку\n"
          "5 - Получить список всех людей на проверку\n"
          "6 - Получить список всех групп работников")

    n = input()
    while not (n and n.isdigit() and 1 <= int(n) <= len(funs)):
        print("Ошибка")
        print("1 - Добавить группу работников\n"
              "2 - Удалить группу работников\n"
              "3 - Получить задания для группы работников\n"
              "4 - Добавить людей на проверку\n"
              "5 - Получить всех людей на проверку\n"
              "6 - Получить список всех групп работников")
        n = input()
    n = int(n)

    print()

    funs[n - 1]()

    input()




