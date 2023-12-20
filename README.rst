nexor
=====

Note:
not recommended for GA yet.

The
`nexor`
command tries to help reasonable workflow
for Python
which is build-tool agnostic.

* `nexor relock`: Create `requirements-<...>.txt` files for all extra dependencies,
  and a `requirements.txt` without any extras.
* `nexor env`: Create a virtual environment in `WORKON_HOME`
  or, if one already exists,
  install the dependencies in it from the lock file.
  By default this is `requirements.txt`,
  but you can configure in
  `pyproject.toml`
  under
  `tools.nexor`
  default_extra to be something else.
* `nexor depend`: Add a dependency to `pyproject.toml`.
  Also,
  by default,
  relock the files
  and update the env.

You can also add new commands to nexor.
[more docs here about how to do it.]
