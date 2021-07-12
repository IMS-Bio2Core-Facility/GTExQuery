# Source Code

```{admonition} Warning: Refactoring Underway!
:class: warning

The source code continues to undergo refactoring to separate data_handling
from multithreading as much as possible.
I'm endeavouring to do so without a breaking change,
but there are no quarantees.
```


The source code is currently divided into 3 modules:

- `logs` submodule, containing code related to logging configuration.
  See [logs](./logging.md).
- `data_handling` contains the code for manipulating query data.
  See [data_handling](./data_handling.md).
- `multithreading` submodule, containing code related to concurrency.
  See [multithreading](./multithreading.md).

```{toctree}
:hidden:
:maxdepth: 3

logging
data_handling
multithreading
```
