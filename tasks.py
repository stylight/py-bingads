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

    # FIXME
    with ctx.shell.root_dir():
        ctx.run(ctx.c('%s --rcfile pylintrc %s', exe, ctx.package),
                echo=True)


@_invoke.task
def deps(ctx):
    ctx.run('pip install -r development.txt', echo=True)


@_invoke.task
def gendocs(ctx):
    ctx.run('sphinx-build docs docs/_build')


@_invoke.task(clean)
def test(ctx):
    """ Run the test suite and measure code coverage. """
    with ctx.shell.root_dir():
        command = ['py.test', '-c', 'test.ini', '-vv', '-s',
                   '--doctest-modules', '--color=yes', '--exitfirst']
        options = [
            ctx.c('--cov=%(package)s', package=ctx.package),
            '--cov-config=test.ini',
            '--cov-report=html',
            '--no-cov-on-fail',
        ]
        ctx.run(' '.join(command + options), echo=True)


@_invoke.task
def tox(ctx, rebuild=False, env=None, hashseed=None):
    """ Run the test suite using tox """
    exe = ctx.shell.frompath('tox')
    if exe is None:
        raise RuntimeError("tox not found")
    args = [exe]

    cmd = '%s -c test.ini'
    if rebuild:
        cmd += ' -r'
    if env is not None:
        cmd += ' -e %s'
        args.append(env)

    if hashseed is not None:
        cmd += ' --hashseed %s'
        args.append(hashseed)

    with ctx.shell.root_dir():
        ctx.run(ctx.c(cmd, *args), echo=True)


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
namespace.add_task(test)
namespace.add_task(tox)
