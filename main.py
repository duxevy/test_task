import os
import re
import csv
import argparse
import pyautogui

from datetime import datetime
from subprocess import Popen
from time import sleep
from configparser import ConfigParser


def get_args() -> dict:
    """
    Parse arguments from terminal
    :return: args_dict -> dict
    {
        "path": <path to .kkrieger>
        "output: <path to output dir> [optional] default: ./test_results
    }
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to execution file (path to .kkrieger)")
    parser.add_argument("-o", "--output", nargs="?", default="./test_results",
                        help="[optional] Path to save test results. Default: ./ test_results")
    args = parser.parse_args()
    if not os.path.exists(args.path):
        raise FileNotFoundError("Wrong path")
    if not os.path.exists(args.output):
        os.mkdir(args.output)
    args_dict = vars(args)

    return args_dict


def get_config() -> dict:
    """
    Parse config.ini file on root dir

    :return: fraps_config -> dict
    {
    "fraps_path": <path to FRAPS directory>,
    "fraps_output": <path to FRAPS Benchmark dir>,
    "fraps_hotkey": <FRAPS start FPS benchmark hotkey> default: "f11"
    }
    """
    config = ConfigParser()
    config.read('config.ini')
    fraps_config = {
        'fraps_path': config['fraps config']['fraps_path'],
        'fraps_output': config['fraps config']['fraps_output'],
        'fraps_hotkey': config['fraps config']['fraps_benchmark_hotkey']
    }

    return fraps_config


def get_screen_size() -> tuple:
    """
    Get user display size
    :return: screen_width, screen_height -> tuple
    (1920, 1080)
    """

    screen_width, screen_height = pyautogui.size()

    return screen_width, screen_height


def launch_game(exec_file: str, screen_size: tuple) -> Popen:
    """
    1. Launch .kkrieger via subprocess.Popen
    2. Waiting while pixel in the middle of screen gets not white or black (loading screen colors)
    3. Get into a game pressing on buttons via pyautogui's keyUp and keyDown
    :param exec_file: str: get_args().get("path")
    :param screen_size: tuple: get_screen_size()
    :return: subprocess.Popen
    """
    game_process = Popen([os.path.normpath(exec_file), "-f"])
    print(f"Game launched at {datetime.now()}")
    width, height = screen_size
    sleep(5)
    flag = True
    while flag:
        sleep(.5)
        pix = pyautogui.pixel(width // 2, height // 2)
        if pix[0] not in (0, 255):
            flag = False
    print(f"Game loaded: {datetime.now()}")
    sleep(1)
    pyautogui.keyDown('esc')
    pyautogui.keyUp('esc')
    sleep(1)
    pyautogui.keyDown('enter')
    pyautogui.keyUp('enter')
    print(f"Scene loaded: {datetime.now()}")
    return game_process


def launch_fraps(path: str) -> Popen:
    """
    Launch FRAPS
    :param path: str: get_config.get("fraps_path")
    :return: subprocess.Popen
    """
    fraps_process = Popen([os.path.normpath(path), "-f"])
    print("FRAPS working")
    return fraps_process


def make_steps() -> None:
    """
    Makes few steps backwards and forward by pressing on the buttons using pyautogui
    :return: None
    """
    pyautogui.keyDown('s')
    sleep(5)
    pyautogui.keyUp('s')
    pyautogui.keyDown('w')
    sleep(5)
    pyautogui.keyUp('w')


def make_screenshot(output_path: str, file_name: str) -> None:
    """
    Makes screenshot by pyautogui and saves them to output path
    :param output_path: get_args().get("output")
    :param file_name: str: name of the screenshot file
    :return: None
    """
    scr = pyautogui.screenshot()
    path = os.path.join(output_path, file_name)
    scr.save(path)
    print('Screenshot captured')


def process_kill(game_process: Popen, fraps_process: Popen) -> None:
    """
    Kills all processes
    :param game_process: launch_game()
    :param fraps_process: launch_fraps()
    :return: None
    """
    game_process.kill()
    sleep(1)
    fraps_process.kill()


def clear_fraps_output(path: str) -> None:
    """
    Clears benchmark statistics from previous sessions
    :param path: path to FRAPS Benchmark logs
    :return: None
    """
    for f in os.listdir(path):
        if re.search(r"(csv)$", f):
            os.remove(os.path.join(path, f))
        else:
            print("CSV file doesn't exist.")


def csv_parser(path: str) -> dict:
    """
    Gets .csv file with FRAPS Benchmark and turns it into Python dictionary
    :param path: path to FRAPS Benchmark logs
    :return: dict_reader -> dict
    """
    for f in os.listdir(path):
        if re.search(r"(csv)$", f):
            with open(os.path.join(path, f), newline='') as file:
                reader = csv.DictReader(file)
                dict_reader: dict
                for row in reader:
                    dict_reader = row
                file.close()
        else:
            pass
    return dict_reader


def get_fps_avg(source: dict, path: str):
    """
    Write to .txt file average FPS for the last session
    :param source: FRAPS benchmark log on dict
    :param path: where to save the file
    :return:
    """
    with open(os.path.join(os.path.normpath(path), 'average_fps.txt'), 'w') as file:
        file.write(f"Average FPS on session: {source.get(' Avg')}")
        file.close()


def script():
    """
    Runs whole script
    :return: None
    """
    args = get_args()
    config = get_config()
    clear_fraps_output(config.get("fraps_output"))
    fraps_process = launch_fraps(config.get("fraps_path"))
    screen_size = get_screen_size()
    sleep(1)
    game_process = launch_game(args.get("path"), screen_size)
    sleep(.7)
    make_screenshot(get_args().get("output"), 'screenshot1.png')
    pyautogui.keyDown(config.get("fraps_hotkey"))
    pyautogui.keyUp(config.get("fraps_hotkey"))
    make_steps()
    pyautogui.keyDown(config.get("fraps_hotkey"))
    pyautogui.keyUp(config.get("fraps_hotkey"))
    sleep(.7)
    make_screenshot(get_args().get("output"), 'screenshot2.png')
    process_kill(game_process, fraps_process)
    print(f'Test completed: {datetime.now()}')
    fraps_benchmark = csv_parser(config.get("fraps_output"))
    get_fps_avg(fraps_benchmark, args.get("output"))


if __name__ == '__main__':
    script()
