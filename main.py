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


def get_and_del_first_n_people(n: int) -> list:
    f = open_json()

    ret, f["people"] = f["people"][:n], f["people"][n:]
    write_json(f)
    return ret


def get_work_from_date(date: int, count: int) -> list:

    ret = []
    workers = get_workers_from_date(date)

    if len(open_json()["people"]) < count * len(workers):
        raise ValueError("Недостаточно людей на проверку.")

    for i in workers:
        ret += [{
            "worker": i,
            "people": get_and_del_first_n_people(count)
        }]

    return ret


# print(*get_worker_from_date(1), sep="\n")
# add_worker("lolkek", 4)
# add_worker("lolkek1", 4)
# add_worker("lolkek2", 4)
# print(del_worker("lolkek"))

# add_people(["dsdsdsd", "gggg"])
# print(*get_and_del_first_n_people(3))

print(*get_work_from_date(4, 50), sep="\n")



