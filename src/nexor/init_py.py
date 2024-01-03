import pathlib
import sys
from typing import Optional
import subprocess
import logging

import attrs
import hyperlink

from .cli import command, add_argument

LOGGER = logging.getLogger(__name__)

@attrs.frozen
class DetailsBuilder: # pragma: no cover
    name: Optional[str] = attrs.field(default=None)
    organization: Optional[str]= attrs.field(default=None)
    description: Optional[str]= attrs.field(default=None)
    maintainer_name: Optional[str]= attrs.field(default=None)
    maintainer_email: Optional[str]= attrs.field(default=None)
    
    def inform(self, name, value):
        if getattr(self, name) is not None:
            return self
        return attrs.evolve(self, **{name: value})
    
    def data(self):
        res = attrs.asdict(self)
        not_ready = [key for key, value in res.items() if value is None]
        if len(not_ready) != 0:
            raise ValueError("not all values retrieved", not_ready)
        return res
    
def parse_args(db, args): # pragma: no cover
    for field in attrs.fields(type(db)):
        db = db.inform(field.name, getattr(args, field.name))
    return db


def parse_remote(db, git_remote_output): # pragma: no cover
    link = hyperlink.parse(git_remote_output.strip())
    organization, name = link.path[-2:]
    db = db.inform("organization", organization)
    db = db.inform("name", name)
    return db

def parse_user(db, git_user_cofig): # pragma: no cover
    details = dict(
        line.split(None, 1)
        for line in git_user_cofig.splitlines()
    )
    for key, value in details.items():
        db = db.inform("maintainer_" + key.removeprefix("user."), value)
    return db

def get_details(args): # pragma: no cover
    db = parse_args(DetailsBuilder(), args)
    cwd = pathlib.Path(args.env["PWD"])
    try:
        called = args.safe_run(["git", "remote", "get-url", "origin"], cwd=cwd)
    except subprocess.CalledProcessError:
        has_git = False
        LOGGER.info("Git info not available")
    else:
        db = parse_remote(db, called.stdout)
        has_git = True
    called = args.safe_run(["git", "config", "--get-regexp", r"^user\."], cwd=cwd)
    db = parse_user(db, called.stdout)
    return db.data(), has_git

ARGS_TO_FIELDS = dict(
    name="project_name",
    description="short_description",
)

@command(
    add_argument("--no-dry-run", action="store_true", default=False),
    *[
        add_argument("--"+field.name.replace("_", "_"))
        for field in attrs.fields(DetailsBuilder)
    ]
)
def init(args):  # pragma: no cover
    data, has_git = get_details(args)
    args.run(
        [
            sys.executable,
            "-m",
            "copier",
            "copy",
            "gh:moshez/python-standard.git",
            args.env["PWD"],
        ] + [
            f"--data={ARGS_TO_FIELDS.get(key, key)}={value}"
            for key, value in data.items()
        ],
        capture_output=False,
    )
    if not has_git:
        url = f"https://github.com/{data['organization']}/{data['name']}"
        args.run(["git", "init", "."], cwd=args.env["PWD"])
        args.run(["git", "remote", "add", "origin", url], cwd=args.env["PWD"])
        args.run(["git", "commit", "--allow-empty", "-m", "Initial commit"])
        args.run(["git", "push", "--set-upstream", "origin", "trunk"])
