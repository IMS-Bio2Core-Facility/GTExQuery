# Testing

Each module within the source code has its own module for unit testing.
Please see [logging_tests](./logging_tests.md),
[data_handling_tests](./data_handling_tests.md),
and [multithreading_tests](./multithreading_tests.md) for more information.
Additionally,
there is a class-based "fixture" -
well it's not really a fixture,
pytest doesn't allow class based fixtures -
for creating custom temporary file.
Please see [custom_temp_file](./custom_temp_file.md).

```{toctree}
:hidden:
:maxdepth: 3

logging_tests
data_handling_tests
multithreading_tests
custom_temp_file
```
