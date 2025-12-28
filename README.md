# bridge-tc-library

This repository provides utilities for generating duplicate-bridge movements
and managing tournaments, tables, pairs and board groups.

Package layout (PEP 420 namespace package):

- `bridge_tc_library/` (namespace package root)
  - `bws/` — BWS (Board Wise Scoring) helpers and clients
  - `scoring/` — scoring helpers (e.g. `ScoreCalculator`)
  - `structure/` — core domain and movement implementations
    - `core/` — domain datatypes: `Player`, `Pair`, `BoardGroup`, `Position`, `Status`
    - `movements/` — movement generators and strategies
    - `tournament/` — `Tournament`, `Sector`, `Table`, validation

Notes about imports

- Because this project uses a namespace-style layout, import code should refer
  to subpackages explicitly. Example:

  ```py
  from bridge_tc_library.structure.tournament import Tournament
  from bridge_tc_library.structure.core import Pair, Position
  from bridge_tc_library.structure.movements import MovementStrategy
  ```

Setup (recommended)

1. Create virtualenv and activate it:

```bash
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip setuptools wheel
```

2. Install the package editable (this generates egg-info/metadata):

```bash
.venv/bin/python -m pip install -e .
```

3. Optional: install test runner and run tests:

```bash
.venv/bin/python -m pip install pytest
.venv/bin/python -m pytest -q
```

If you prefer not to install, set `PYTHONPATH` to the project root when running
scripts directly:

```bash
PYTHONPATH=$(pwd) python bridge_tc_library/structure/examples/example_strategy.py
```

Why this layout?

- The namespace-style layout keeps the source organized while allowing
  consumers to import the public subpackages directly. It avoids fragile
  top-level re-exports and keeps the package surface explicit.

Troubleshooting

- If an import fails, ensure the editable install succeeded and that your
  venv is activated or `PYTHONPATH` includes the project root.
- When adding new subpackages, keep their module imports explicit under
  `bridge_tc_library.<subpkg>` to avoid accidental reliance on previous
  re-export shims.

Contact

For questions or changes, update the repository or open an issue.
