import argparse
import difflib
import pathlib
import logging

from gather.commands import add_argument
import tomlkit

from . import ENTRY_DATA

LOGGER = logging.getLogger(__name__)


@ENTRY_DATA.register(
    add_argument("--no-dry-run", action="store_true", default=False),
    add_argument("--directory", default="."),
    add_argument("--extra"),
    add_argument("dependency"),
)
def depend(args: argparse.Namespace) -> None:  # pragma: no cover
    original = (pathlib.Path(args.directory) / "pyproject.toml").read_text()
    parsed = tomlkit.loads(original)
    project = parsed["project"]
    if args.extra is None:
        dependencies = project.get("dependencies", [])  # type: ignore
    else:
        dependencies = project.setdefault(  # type: ignore
            "optional-dependencies", {}
        ).setdefault(
            args.extra, []
        )
    if args.dependency not in dependencies:
        dependencies.append(args.dependency)
    revised = tomlkit.dumps(parsed)
    changes = difflib.unified_diff(
        original.splitlines(), revised.splitlines(), lineterm=""
    )
    for line in changes:
        LOGGER.info("Diff: %s", line.rstrip())
    if args.no_dry_run:
        (pathlib.Path(args.directory) / "pyproject.toml").write_text(revised)
    else:
        LOGGER.info("Dry run, not modifiying pyproject.toml")
