import pathlib
import logging

from commander_data.common import LOCAL_PYTHON as PYTHON
from gather.commands import add_argument
import tomlkit

from . import ENTRY_DATA


LOGGER = logging.getLogger(__name__)


def pip_compile(run, dependencies):  # pragma: no cover
    return run(
        PYTHON.module.piptools.compile("-")(output_file="-"),
        input="\n".join(dependencies),
        capture_output=True,
    ).stdout


def lock_dependencies(run, project):  # pragma: no cover
    compiled_dependencies = {}
    dependencies = project.get("dependencies", [])
    all_extras = dict(project.get("optional-dependencies", {}))
    all_extras[""] = []
    for extra, extra_dependencies in all_extras.items():
        all_dependencies = dependencies + extra_dependencies
        compiled_dependencies[extra] = pip_compile(run, all_dependencies)
    return compiled_dependencies


def relock_pyproject(*, safe_run, directory, no_dry_run):  # pragma: no cover
    pyproject = (directory / "pyproject.toml").read_text()
    parsed = tomlkit.parse(pyproject)
    project = parsed["project"]
    locked_contents = lock_dependencies(safe_run, project)
    for name, contents in locked_contents.items():
        if name != "":
            name = "-" + name
        output_file = directory / f"requirements{name}.txt"
        if no_dry_run:
            output_file.write_text(contents)
        else:
            LOGGER.info("Dry run, not relocking", output_file)


@ENTRY_DATA.register(
    add_argument("--no-dry-run", action="store_true", default=False),
    add_argument("--directory", default="."),
)
def relock(args):  # pragma: no cover
    relock_pyproject(
        safe_run=args.safe_run,
        directory=pathlib.Path(args.directory),
        no_dry_run=args.no_dry_run,
    )
