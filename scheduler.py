from typing import List
import requests
from datetime import datetime, timedelta


def validate_date_format(func):
    def wrapper(self, date, *args):
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format. Expected '%Y-%m-%d'")
        return func(self, date, *args)
    return wrapper


class Scheduler:
    def __init__(self, url: str):
        schedule = self._fetch_data(url)
        self.__days: List[dict] = schedule["days"]
        self.__timeslots: List[dict] = schedule["timeslots"]

    def _fetch_data(self, url: str) -> dict:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @validate_date_format
    def get_busy_slots(self, date: str) -> List[tuple[str, str]]:
        result = list()
        day_id = -1
        for day in self.__days:
            if day["date"] == date:
                day_id = day["id"]
                break
        if day_id == -1:
            raise ValueError(f"Date {date} wasn't found")
        for timeslot in self.__timeslots:
            if timeslot["day_id"] == day_id:
                result.append((timeslot["start"], timeslot["end"]))
        return result

    @validate_date_format
    def get_free_slots(self, date: str) -> List[tuple[str, str]]:
        busy_slots = sorted(self.get_busy_slots(date))
        start_time = str()
        end_time = str()
        for day in self.__days:
            if day["date"] == date:
                start_time = day["start"]
                end_time = day["end"]
                break
        result = list()
        last_end = start_time
        for i in range(len(busy_slots)):
            if last_end < busy_slots[i][0]:
                result.append((last_end, busy_slots[i][0]))
            last_end = max(last_end, busy_slots[i][1])
        if last_end < end_time:
            result.append((last_end, end_time))
        return result

    @validate_date_format
    def is_available(self, date: str, start: str, end: str) -> bool:
        try:
            datetime.strptime(start, "%H:%M")
            datetime.strptime(end, "%H:%M")
        except ValueError:
            raise ValueError(f"Invalid time format. Expected '%H:%M'")
        if start > end:
            raise ValueError(
                f"Invalid time input, start must be earlier then end")
        free_slots = self.get_free_slots(date)
        for slot in free_slots:
            if slot[0] <= start and slot[1] >= end:
                return True
            if slot[0] > end:
                break
        return False

    def find_slot_for_duration(self, duration_minutes: int) -> tuple[str, str, str]:
        delta = timedelta(minutes=duration_minutes)
        for day in self.__days:
            for slot in self.get_free_slots(date=day["date"]):
                if delta <= datetime.strptime(slot[1], "%H:%M") - datetime.strptime(slot[0], "%H:%M"):
                    return (day["date"], slot[0], datetime.strftime(datetime.strptime(slot[0], "%H:%M") + delta, "%H:%M"))
        return None
