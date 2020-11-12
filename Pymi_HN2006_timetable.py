__doc__ = """

query_param
         |name        |idBoard     |idList
board    |required    |            |
list     |required    |required    |
card     |optinal     |            |required

"""

import requests
import datetime
import json

with open("secret.json") as f:
    secret = json.load(f)


class Trello:
    def __init__(self):
        self.url = {
            "board": f"https://api.trello.com/1/boards",
            "list": f"https://api.trello.com/1/lists",
            "card": f"https://api.trello.com/1/cards",
        }
        self.key = secret["TRELLO_KEY"]
        self.token = secret["TRELLO_TOKEN"]

    def create_object(self, obj, **params):
        url = self.url[obj]

        query = {"key": self.key, "token": self.token}

        for key in params.keys():
            query[key] = params[key]

        response = requests.request("POST", url, params=query)

        return response.json()


def all_dates():
    start_day = datetime.date(2020, 6, 25)
    five_days = datetime.timedelta(days=5)
    a_week = datetime.timedelta(days=7)
    result = []

    for i in range(12):
        if i % 2 == 0:
            result.append(
                (start_day + a_week * (i // 2)).strftime(f"%Y-%m-%d") + "T14:30:00.000Z"
            )
        else:
            result.append(
                (start_day + a_week * (i // 2) + five_days).strftime(f"%Y-%m-%d")
                + "T14:30:00.000Z"
            )

    return result


def solve():
    trello = Trello()

    try:
        params = {
            "name": "Học Python Hà Nội PYMI.vn HN2006 timetable",
            "prefs_permissionLevel": "public",
            "prefs_background": "orange",
        }
        Board = trello.create_object("board", **params)
        print("Board created")
    except:
        print("Somethings wrong with creating Board")

    try:
        Lists = [
            trello.create_object("list", **{"name": name, "idBoard": Board["id"]})
            for name in ["Thứ 3", "Thứ 5"]
        ]
        print("Lists created")
    except:
        print("Somethings wrong with creating List")

    try:
        dates = all_dates()

        for lesson in range(1, 13):
            if lesson % 2 == 1:
                name = "Bài " + str(lesson)
                params = {
                    "name": name,
                    "idList": Lists[1]["id"],
                    "due": dates[lesson - 1],
                }
                trello.create_object("card", **params)
            else:
                params = {
                    "name": name,
                    "idList": Lists[0]["id"],
                    "due": dates[lesson - 1],
                }
                trello.create_object("card", **params)
        print("Cards created")
    except:
        print("Somethings wrong with creating Cards")


def main():
    solve()


if __name__ == "__main__":
    main()
