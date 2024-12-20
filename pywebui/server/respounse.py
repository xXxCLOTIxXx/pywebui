from os import path as p
from flask import render_template_string, render_template, jsonify, send_from_directory
from typing import Any


def render_template_path(path, **context: Any) -> str:
    if p.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            return render_template_string(file.read(), **context)
    raise FileNotFoundError(path)