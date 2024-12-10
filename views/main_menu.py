# full docs: https://inquirerpy.readthedocs.io/en/latest/

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator


def show_main_menu():
    action = inquirer.select(
        message="\nMAIN MENY.\nSelect an action:",
        choices=[
            "Work with readers",
            "Work with catalogue",
            Choice(value=None, name="Exit"),
        ],
        default=None,
    ).execute()
    if action:
        region = inquirer.select(
            message="Select regions:",
            choices=[
                Choice("ap-southeast-2", name="Sydney"),
                Choice("ap-southeast-1", name="Singapore"),
                Separator(),
                "us-east-1",
                "us-east-2",
            ],
            multiselect=True,
            transformer=lambda result: f"{len(result)} region{'s' if len(result) > 1 else ''} selected",
        ).execute()
    
