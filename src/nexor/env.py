import os
import pathlib
import shutil

from commander_data import COMMAND
from commander_data.common import BASE_PYTHON
from gather.commands import add_argument

from . import ENTRY_DATA


def parse_packages(contents):  # pragma: no cover
    def inner_parse():
        for a_line in contents.splitlines():
            a_line = (" " + a_line).split("#", 1)[0].strip()
            if a_line == "":
                continue
            if a_line.startswith("-e "):
                continue
            package, version = a_line.split("==")
            yield package.lower().replace("_", "-").replace(".", "-"), version

    return dict(inner_parse())


def python_module(env_path):  # pragma: no cover
    return COMMAND(os.fspath(env_path / "bin" / "python"))(m=None)


def should_destroy(args, env_path, packages_to_install):  # pragma: no cover
    if args.force_recreate:
        return True
    python = env_path / "bin" / "python"
    if not python.exists():
        return False
    res = args.safe_run(python_module(env_path).pip.freeze, capture_output=True)
    try:
        old_packages = parse_packages(res.stdout)
    except ValueError:
        return True
    unneeded_packages = set(old_packages) - set(packages_to_install)
    return len(unneeded_packages) != 0


@ENTRY_DATA.register(
    add_argument("--no-dry-run", action="store_true", default=False),
    add_argument("--force-recreate", action="store_true", default=False),
)
def env(args):  # pragma: no cover
    pwd = pathlib.Path(args.env["PWD"])
    requirements = pwd / "requirements-tests.txt"
    packages_to_install = parse_packages(requirements.read_text())
    try:
        root_path = pathlib.Path(args.env["WORKON_HOME"])
    except KeyError:
        root_path = pathlib.Path(args.env["HOME"]) / ".virtualenvs"
    env_path = root_path / pwd.name
    if should_destroy(args, env_path, packages_to_install):
        if args.no_dry_run:
            shutil.rmtree(env_path)
        else:
            print("Dry run, not removing environment", env_path)
    if not env_path.exists():
        args.run(
            BASE_PYTHON.module.venv(os.fspath(env_path)),
        )
    args.run(
        python_module(env_path).pip.install(
            r=os.fspath(requirements),
            e=args.env["PWD"],
        )
    )
