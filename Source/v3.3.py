"""A simple script to show Islamic prayer and related times for Tehran (Tajrish), Iran.  Times related to my working hours are highlighted.  DLord"""

import os
import sys
from datetime import date
import requests
from art import tprint
from persiantools.jdatetime import JalaliDate

SCRIPT_VERSION = '3.3'
WINDOW_TITLE = f"Islamic Prayer Times by DLord (version {SCRIPT_VERSION})"


def set_window_title(title: str) -> None:
    """Set the window title for the console."""
    if os.name == 'nt':
        os.system(f'title {title}')
    else:
        os.system(f'PS1="\[\e]0;{title}\a\]"; echo $PS1')


def clear_console() -> None:
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_date() -> str:
    """Get todays date and retuen formated string."""
    today = date.today()
    return '\033[1;34m' + today.strftime("%A %d-%b-%y") + '\033[0m'


def get_jalali_date() -> str:
    """Get todays date based on Jalali Calendar and return formated string."""
    months = {
        '1': 'Farvardin',
        '2': 'Ordibehesht',
        '3': 'Khordad',
        '4': 'Tir',
        '5': 'Mordad',
        '6': 'Shahrivar',
        '7': 'Mehr',
        '8': 'Aban',
        '9': 'Azar',
        '10': 'Day',
        '11': 'Bahman',
        '12': 'Esfand',
    }
    jdate = str([JalaliDate.today()])[12:-2]
    jlist = jdate.replace(' ', '').split(',')
    todayJ = jlist[3] + ', ' + jlist[2] + \
        ' ' + months[jlist[1]] + ', ' + jlist[0]
    return '\033[1;91m' + todayJ + '\033[0m'


def ascii_art() -> None:
    """Print an ascii art with random font of author's name"""
    author = "DLord"
    tprint("\n\n" + author, font="random")


if __name__ == '__main__':
    set_window_title(WINDOW_TITLE)
    clear_console()

    try:
        response = requests.get(
            "http://api.aladhan.com/v1/timingsByAddress?address=Tajrish%2C+Tehran%2C+Iran&method=7&midnightMode=1", timeout=10)
        response.raise_for_status()
        timings = response.json()['data']['timings']
        print('Azan times for: ', get_date(), ' -', get_jalali_date())
        print(
            f"\nAzan Sobh: \033[1m{timings['Fajr']}\033[0m\nSunrise: \033[1m{timings['Sunrise']}\033[0m\nAzan Zohr: \033[1;46m{timings['Dhuhr']}\033[0m\nAzan Asr: \033[1;46m{timings['Asr']}\033[0m\nSunset: \033[1m{timings['Sunset']}\033[0m\nAzan Maghreb: \033[1;46m{timings['Maghrib']}\033[0m\nAzan Ashaa: \033[1;46m{timings['Isha']}\033[0m\nMidnight: \033[1m{timings['Midnight']}\033[0m")
        ascii_art()
        input("\nPress Enter to Exit...")
    except (requests.exceptions.RequestException, ValueError) as e:
        sys.exit(f"An error occurred: {e}")
    except KeyboardInterrupt:
        sys.exit("\nScript terminated by user.")
