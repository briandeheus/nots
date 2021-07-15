import tempfile, os
from subprocess import call

EDITOR = os.environ.get("EDITOR", "vim")  # that easy!
ARG = "@editor"
initial_message = ""  # if you want to set up the file somehow


def open_editor(field_name):
    with tempfile.NamedTemporaryFile(suffix=".tmp", prefix=f"{field_name}-") as temp:
        call([EDITOR, temp.name])
        temp.seek(0)
        return temp.read().decode().strip()
