#! /usr/bin/env python3

import math
import notify2
import sys
import time

POMODORO_LENGTH = 25 * 60 # seconds
PAUSE_LENGTH = 5 * 60 # seconds
BREAK_LENGTH = POMODORO_LENGTH + PAUSE_LENGTH # seconds
COUNTDOWN_GRANULARITY = 1 # seconds

def prompt(choices):
    while True:
        print("What's your mood?")
        for choice in choices:
            print(f'{choice}: {choices[choice]}')

        choice = input().strip()
        if choice not in choices:
            print(f'"{choice}" isn\'t a valid choice!')
            continue

        return choice

def notify(message):
    print(message)
    notify2.Notification(message).show()

def countdown(duration):
    start = time.time()
    while True:
        elapsed = time.time() - start
        remaining = max(0, math.floor(duration - elapsed))

        print(f'\r{remaining // 60}:{remaining % 60:02}\033[K', end='')

        if remaining <= 0:
            print()
            return

        time.sleep(min(COUNTDOWN_GRANULARITY, remaining))

def prompt_and_run():
    while True:
        choice = prompt({'1': '🍅', '2': '☕'})

        if choice == '1':
            do_a_pomodoro()
        elif choice == '2':
            take_a_break()

def do_a_pomodoro():
    notify("💨 Get crackin'!")
    countdown(POMODORO_LENGTH)
    notify("🍅 Pomodoro's over! Ready for a pause?")
    countdown(PAUSE_LENGTH)
    notify("⏰ Back to work, slacker!")

def take_a_break():
    notify("☕ Tea time!")
    countdown(BREAK_LENGTH)
    notify("⏰ Back to work, slacker!")

def main():
    notify2.init('Pomo')

    try:
        prompt_and_run()
    except (EOFError, KeyboardInterrupt):
        return

if __name__ == '__main__':
    sys.exit(main())
