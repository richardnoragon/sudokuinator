# Naming and migration

The public product is Sudoku-inator, the distribution and launch command are
`sudoku-inator`, and the Python package is `sudoku_inator`.
The repository is hosted at
[richardnoragon/sudokuinator](https://github.com/richardnoragon/sudokuinator).

## Updating a development checkout

Use the installation steps in [README.md](README.md#install-and-run). Replace
old `richards_sudoku` imports with `sudoku_inator` and use the `sudoku-inator`
command. The previous import path and command are retired; no alias is promised.
A checkout folder's name does not determine the Python import path.

Existing remotes using the former `sudoku-inator` repository URL may redirect;
use the current repository URL for new clones. The package name still contains
the hyphen. Tests use the current package imports.

## Saved games

The rebrand did not change the application version or save schema. The current
application reads versions 1 and 2 and writes version 2. Keep backups before
upgrading and follow [MIGRATIONS.md](MIGRATIONS.md) for compatibility details.
