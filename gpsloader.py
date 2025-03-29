import os
from datetime import datetime
import pytz

from surveyloader import get_rows
from user import User
from userfactory import UserFactory


def is_night(time: str) -> bool:  # returns true if timestamp is after 10pm or before 4am
    time = get_est(time)
    hour = time.hour
    return hour >= 22 or hour <= 5


def get_est(time: str) -> datetime:
    time = int(time)
    utc_time = datetime.utcfromtimestamp(time)
    est_timezone = pytz.timezone('America/New_York')
    est_time = utc_time.replace(tzinfo=pytz.utc).astimezone(est_timezone)
    return est_time


class GPSLoader:

    def __init__(self, userbase: UserFactory):
        self.userbase = userbase

    def load_user_data(self, folder_path):
        self.find_homes(folder_path)
        self.find_home_times(folder_path)
        return

    def find_homes(self, folder_path): #find homes for all users
        for filename in os.listdir(folder_path):
            uid = int(filename[5:7])
            user = self.userbase.get_user(uid)
            file_path = os.path.join(folder_path, filename)
            rows = get_rows(file_path)
            user.home = self.find_home(rows)

        return

    def find_home_times(self, folder_path): # find avg time at home for all users
        for filename in os.listdir(folder_path):
            uid = int(filename[5:7])
            user = self.userbase.get_user(uid)
            file_path = os.path.join(folder_path, filename)
            rows = get_rows(file_path)
            user.avg_time_at_home = self.find_home_time(rows,user)

        return

    def find_home_time(self, rows: list[list[str]], user: User) -> float:
        HOME_PRECISION = 0.001
        daily_home_times = {}

        current_day = None
        day_home_time = 0.0
        last_home_timestamp = None

        for i in range(1, len(rows)):
            row = rows[i]
            timestamp = row[0]
            lat = float(row[4])
            long = float(row[5])

            est_time = get_est(timestamp)
            day_key = est_time.date()
            is_at_home = (abs(lat - user.home[0]) < HOME_PRECISION and abs(long - user.home[1]) < HOME_PRECISION)
            if current_day is None:
                current_day = day_key
            if day_key != current_day:
                if current_day is not None:
                    daily_home_times[current_day] = day_home_time
                current_day = day_key
                day_home_time = 0.0
                last_home_timestamp = None
            if is_at_home:
                if last_home_timestamp is not None:
                    time_diff = int(timestamp) - last_home_timestamp
                    day_home_time += time_diff / 3600  # Convert to hours

                last_home_timestamp = int(timestamp)
        if current_day is not None and day_home_time > 0:
            daily_home_times[current_day] = day_home_time

        if daily_home_times:
            return sum(daily_home_times.values()) / len(daily_home_times)

        return 0.0

    def find_home(self, rows: list[list[str]]) -> tuple[float, float]:
        GPS_PRECISION = 0.001
        night_location_data = {}

        for i in range(1, len(rows)):
            row = rows[i]
            time = row[0]
            lat = float(row[4])
            long = float(row[5])
            if is_night(time):
                matched_location = None
                for existing_loc in night_location_data.keys():
                    if abs(lat - existing_loc[0]) < GPS_PRECISION and abs(long - existing_loc[1]) < GPS_PRECISION:
                        matched_location = existing_loc
                        break
                if matched_location is None:
                    matched_location = (lat, long)
                if matched_location not in night_location_data:
                    night_location_data[matched_location] = {
                        'count': 1,
                        'total_time': 0
                    }
                else:
                    night_location_data[matched_location]['count'] += 1
                if i < len(rows) - 1:
                    next_time = int(rows[i + 1][0])
                    current_time = int(time)
                    time_diff = next_time - current_time
                    night_location_data[matched_location]['total_time'] += time_diff

        def location_score(location_data):
            count_weight = 0.5
            time_weight = 0.5
            max_count = max(data['count'] for data in night_location_data.values())
            max_time = max(data['total_time'] for data in night_location_data.values())

            normalized_count = location_data['count'] / max_count
            normalized_time = location_data['total_time'] / max_time

            return count_weight * normalized_count + time_weight * normalized_time
        best_location = max(night_location_data,key=lambda loc: location_score(night_location_data[loc]))
        return best_location
