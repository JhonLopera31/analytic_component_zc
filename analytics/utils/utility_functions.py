from json import load
from pathlib import Path
from typing import Any


def json_message(msn: str) -> dict:
    return {"Message": f"{msn}"}


def create_folder_if_not_exist(path: Path):
    try:
        path.mkdir(parents=True, exist_ok=False)
        print("--- Folder was created")
    except FileExistsError:
        print("--- Folder is already there")


def read_json_file_from(path: str) -> list:
    with open(path, "r") as file_object:
        json_data = load(file_object)
    return json_data
