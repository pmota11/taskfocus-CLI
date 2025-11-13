import argparse
import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("tasks.json")


def load_tasks():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def add_task(title, priority):
    tasks = load_tasks()
    task = {
        "id": tasks[-1]["id"] + 1 if tasks else 1,
        "title": title,
        "priority": priority,
        "done": False,
        "created_at": datetime.now().isoformat(timespec="seconds")
    }
    tasks.append(task)
    save_tasks(tasks)


def list_tasks(show_done):
    tasks = load_tasks()
    filtered = tasks if show_done else [t for t in tasks if not t["done"]]
    if not filtered:
        print("Nenhuma tarefa encontrada.")
        return
    for t in filtered:
        status = "✔" if t["done"] else "•"
        print(f'{t["id"]:03d} {status} [{t["priority"].upper()}] {t["title"]} ({t["created_at"]})')


def complete_task(task_id):
    tasks = load_tasks()
    updated = False
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            updated = True
            break
    if not updated:
        print("Tarefa não encontrada.")
        return
    save_tasks(tasks)


def remove_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print("Tarefa não encontrada.")
        return
    save_tasks(new_tasks)


def build_parser():
    parser = argparse.ArgumentParser(prog="taskfocus")
    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add")
    p_add.add_argument("title")
    p_add.add_argument("-p", "--priority", choices=["baixa", "media", "alta"], default="media")

    p_list = sub.add_parser("list")
    p_list.add_argument("--all", action="store_true")

    p_done = sub.add_parser("done")
    p_done.add_argument("id", type=int)

    p_rm = sub.add_parser("rm")
    p_rm.add_argument("id", type=int)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title, args.priority)
    elif args.command == "list":
        list_tasks(args.all)
    elif args.command == "done":
        complete_task(args.id)
    elif args.command == "rm":
        remove_task(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
