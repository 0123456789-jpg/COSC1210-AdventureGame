import json
import os
from typing import Union


def main() -> None:
    with open(os.path.join("src", "main.py")) as py, open(
        os.path.join("src", "main.ipynb"), "w"
    ) as ipynb:
        notebook: dict[str, Union[list[object], dict[str, object], int]] = {
            "cells": [{"cell_type": "code", "metadata": {}, "source": py.read()}],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                },
                "language_info": {"name": "python", "version": "3.9.5"},
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        json.dump(notebook, ipynb)
    print("Done.")


main()
