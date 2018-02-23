#!/usr/bin/env python
""" Invoke tasks. """
import invoke as _invoke

import _shell


@_invoke.task
def clean(ctx):
    """ Wipe *.py[co] files and test leftovers """
    for name in ctx.shell.files('.', '.coverage*', recursive=False):
        ctx.shell.rm(name)

    ctx.shell.rm('pytest.xml', 'coverage.xml')
    ctx.shell.rm_rf(
        '_coverage',
        'build',
        'dist',
    )


@_invoke.task(clean)
def lint(ctx):
    exe = ctx.shell.frompath('pylint')
    if exe is None:
        raise RuntimeError("pylint not found")

    with ctx.shell.root_dir():
        ctx.run(ctx.c('%s --rcfile pylintrc %s', exe, ctx.package),
                echo=True)


@_invoke.task
def deps(ctx):
    ctx.run('pip install -r development.txt', echo=True)


@_invoke.task
def gendocs(ctx):
    ctx.run("sphinx-build docs docs/_build")


env = dict(
    package='py_bingads',
    shell=dict(
        (key, value) for key, value in vars(_shell).items()
        if not key.startswith('_')
    ),
    c=_shell.command,
)

namespace = _invoke.Collection()
namespace.configure(env)
namespace.add_task(clean)
namespace.add_task(lint)
namespace.add_task(deps)


