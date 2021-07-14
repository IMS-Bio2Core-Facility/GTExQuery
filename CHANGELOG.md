# Changelog

<!--next-version-placeholder-->

## v1.0.0 (2021-07-14)
### Feature
* **data_handling:** Change process output to csv ([`98f6225`](https://github.com/IMS-Bio2Core-Facility/GTExQuery/commit/98f622531a2ef9597cff58de56ef840a6cb6a603))

### Breaking
* Real-world tests showed that it was quite challenging, if not impossible, to create two excel files that could be compared on a byte-by-byte level and be identical, even if their content was the same by eye. To obliviate this, and easing pipeline testing, the decision was made to move to the more reliable (and transparent) csv format.  ([`98f6225`](https://github.com/IMS-Bio2Core-Facility/GTExQuery/commit/98f622531a2ef9597cff58de56ef840a6cb6a603))

### Documentation
* **README:** Correct links to GTExSnake ([`5cec877`](https://github.com/IMS-Bio2Core-Facility/GTExQuery/commit/5cec877cd45bc81547dd00d398560afcad12fb04))
* **sphinx:** Remove multithreading.process module ([`7b0eb83`](https://github.com/IMS-Bio2Core-Facility/GTExQuery/commit/7b0eb835a3dcb50f11809a4208ed6b47d176ed4d))

## v0.2.2 (2021-07-12)
### Fix
* **multithreading:** Correct relative imports ([`3285559`](https://github.com/IMS-Bio2Core-Facility/GTExQuery/commit/328555968deb74c6ef44280a5ce125c17f1765d0))

## v0.2.1 (2021-07-12)
### Fix
* **BMSession:** Change cache to False ([`1ce9c51`](https://github.com/IMS-Bio2Core-Facility/GTExQuery/commit/1ce9c5115fa6fc81573de79c6cd84512c94f86d2))

### Documentation
* **README:** Add PyPi badge ([`e9adb9d`](https://github.com/IMS-Bio2Core-Facility/GTExQuery/commit/e9adb9d2d1aeafbdc16fd37d923690a6a938da9e))
* **sphinx:** Add changelog to doc build ([`afe2ce4`](https://github.com/IMS-Bio2Core-Facility/GTExQuery/commit/afe2ce465d9e824db552a276b141d362b279a761))

## v0.2.0 (2021-07-12)
### Feature
* **repo:** Initiate repository ([`93b88cf`](https://github.com/IMS-Bio2Core-Facility/GTExQuery/commit/93b88cf2b2928f8d36718f4b9bb0e3f8ece9fd48))

### Documentation
* **docs:** Correct links throughout ([`e60fc02`](https://github.com/IMS-Bio2Core-Facility/GTExQuery/commit/e60fc02047bca90ff4b23c611c654ab2208b84a2))
* **gtexquery:** Add module docstring ([`73669ed`](https://github.com/IMS-Bio2Core-Facility/GTExQuery/commit/73669ed0f29c8c9b0da69860b31d5aa6d03a01e3))
