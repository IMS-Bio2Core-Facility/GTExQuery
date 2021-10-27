# GTExQuery

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9](https://img.shields.io/badge/Python-3.9-brightgreen.svg)](https://docs.python.org/3/whatsnew/3.9.html)
[![Status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![CI/CD](https://github.com/IMS-Bio2Core-Facility/GTExQuery/actions/workflows/main.yml/badge.svg)](https://github.com/IMS-Bio2Core-Facility/GTExQuery/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/IMS-Bio2Core-Facility/GTExQuery/branch/main/graph/badge.svg?token=L56T1KFL1J)](https://codecov.io/gh/IMS-Bio2Core-Facility/GTExQuery)
[![Documentation Status](https://readthedocs.org/projects/gtexquery/badge/?version=latest)](https://gtexquery.readthedocs.io/en/latest/)
[![Codestyle: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI](https://img.shields.io/pypi/v/gtexquery)](https://pypi.org/project/gtexquery/)

```{admonition} For use with GTExSnake
:class: tip

This repository houses the code, tests, etc.,
that run the nuts and bolts of the Snakemake pipeline
[GTExSnake][GTExSnake]
```

GTExSnake is a fully concurrent pipeline for querying
transcript-level GTEx data in specific tissues.
This package handles all the code needed for
multithreading,
data handling,
and file manipulation necessary for so-said pipeline.

If you find the project useful,
leaves us a star on [github][stars]!

If you want to contribute,
please see the [guide on contributing](contributing.md)

## Motivation

There are a number of circumstances where transcript level expressed data for a
specific tissue is highly valuable.
For tissue-dependent expression data,
there are few resources better than GTEx.
In this case, the `medianTranscriptExpression` query provides the necessary data.
It returns the median expression of each transcript for a gene in a given tissue.

As the code and tests necessary to handle the multithreading and data grew,
maintaining both the pipeline and the source code in a single repository
became quite the challenge.
To help alleviate this,
it was decided to refactor the source code into its own repository,
allowing both the pipeline and the code to more easily adhere to best practices.

## Further Information

For more information about the source code,
see our [documentation][docs] on ReadTheDocs.
You can learn more about the pipeline this code supports [here][GTExSnake].

[GTExSnake]: https://github.com/IMS-Bio2Core-Facility/GTExSnake "GTExSnake Snakemake Pipeline"
[stars]: https://github.com/IMS-Bio2Core-Facility/GTExQuery/stargazers "Stargazers"
[docs]: https://gtexquery.readthedocs.io/en/latest/ "Package Documentation"
