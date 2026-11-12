#!/usr/bin/env python3
"""Tiny habit tracker CLI. Habits live in habits.json next to this file."""
import argparse
import json
import os
import sys
from datetime import date, timedelta

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "habits.json")


def load():
    if not os.path.exists(DB):
        return []
    with open(DB, encoding="utf-8") as f:
        return json.load(f)


def save(habits):
    with open(DB, "w", encoding="utf-8") as f:
        json.dump(habits, f, indent=2)


def cmd_add(args):
    habits = load()
    habits.append({"id": (habits[-1]["id"] + 1 if habits else 1),
                   "name": args.name, "done": {}})
    save(habits)
    print("Added habit:", args.name)


def cmd_list(args):
    habits = load()
    today = date.today().isoformat()
    if not habits:
        print("No habits yet.")
        return
    for h in habits:
        mark = "x" if h["done"].get(today) else " "
        print("[%s] %d %s" % (mark, h["id"], h["name"]))


def cmd_check(args):
    habits = load()
    today = date.today().isoformat()
    for h in habits:
        if h["id"] == args.id:
            h["done"][today] = True
            save(habits)
            print("Checked off:", h["name"])
            return
    print("No habit with id", args.id, file=sys.stderr)
    sys.exit(1)


def cmd_rename(args):
    habits = load()
    for h in habits:
        if h["id"] == args.id:
            h["name"] = args.name
            save(habits)
            print("Renamed to:", args.name)
            return
    print("No habit with id", args.id, file=sys.stderr)
    sys.exit(1)


def main():
    p = argparse.ArgumentParser(prog="habit")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("name")
    a.set_defaults(fn=cmd_add)
    li = sub.add_parser("list")
    li.set_defaults(fn=cmd_list)
    c = sub.add_parser("check")
    c.add_argument("id", type=int)
    c.set_defaults(fn=cmd_check)
    r = sub.add_parser("rename")
    r.add_argument("id", type=int)
    r.add_argument("name")
    r.set_defaults(fn=cmd_rename)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
