import pathlib
import subprocess
import sys

import tomlkit

from .cli import command, add_argument

compilation_command = [
    sys.executable,
    "-m",
    "piptools",
    "compile",
    "-",
    "--output-file=-",
]

def pip_compile(run, dependencies):
    input_data = "\n".join(dependencies)
    result = run(
        compilation_command,
        input=input_data,
        capture_output=True,
    )
    return result.stdout

def lock_dependencies(run, project):
    compiled_dependencies = {}
    dependencies = project["dependencies"]
    for extra, extra_dependencies in project["optional-dependencies"].items():
        all_dependencies = dependencies + extra_dependencies
        compiled_dependencies[extra] = pip_compile(run, all_dependencies)
    return compiled_dependencies

def relock_pyproject(*, run, directory,  no_dry_run):
    pyproject = (directory / "pyproject.toml").read_text()
    parsed = tomlkit.parse(pyproject)
    project = parsed["project"]
    locked_contents = lock_dependencies(run, project)
    if no_dry_run:
        for name, contents in locked_contents.items():
            (directory / f"requirements-{name}.txt").write_text(contents)
    else:
        print("Dry run, not relocking")

@command(
    add_argument("--no-dry-run", action="store_true", default=False),
    add_argument("--directory", default="."),
)
def relock(args):
    relock_pyproject(
        run=args.run,
        directory=pathlib.Path(args.directory),
        no_dry_run=args.no_dry_run,
    )