#!/bin/bash

function script_path () {
	path="$(realpath "${BASH_SOURCE:-$0}")"
	echo "$(dirname "$path")"
}

venv_dir="$(script_path)/venv"
activate="$venv_dir/bin/activate"

python -m venv "$venv_dir"
source "$activate"
pip install -r "$(script_path)/requirements.txt"
deactivate
