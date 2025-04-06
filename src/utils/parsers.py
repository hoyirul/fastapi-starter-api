# src/utils/parsers.py
# -*- coding: utf-8 -*-
# Copyright 2024 - Ika Raya Sentausa

from datetime import datetime


class Parser:
    def __init__(self, params: str = ""):
        self.params = params

    # calelcase
    def camelcase(self) -> str:
        return self.params.replace(" ", "").title()

    # snakecase
    def snakecase(self) -> str:
        return self.params.replace(" ", "_").lower()

    # kebabcase
    def kebabcase(self) -> str:
        return self.params.replace(" ", "-").lower()

    # pascalcase
    def pascalcase(self) -> str:
        return self.params.replace(" ", "").title()

    # titlecase
    def titlecase(self) -> str:
        return self.params.title()

    # sentencecase
    def sentencecase(self) -> str:
        return self.params.capitalize()

    # constantcase
    def constantcase(self) -> str:
        return self.params.replace(" ", "_").upper()

    # make code from string ex. "Hello World" -> "HW" just 2 character, ex. "Hello World Exam" -> "HW" not "HWE"
    def journal_code(self) -> str:
        return "".join([i[0] for i in self.params.split()]).upper()

    def timestamp(self) -> str:
        return f"{datetime.now().strftime('%y%m%d/%H%M%S')}{datetime.now().strftime('%f')[:3]}"
