=======
Changes
=======

0.1.2 / 2020-05-19
==================

* Round input seconds in format_mins to avoid weird numbers such as 0m60s when the input is 59.9
  (after this patch the example above returns 1m00s)
* Fix timer so it will keep report aligned when the time exceeds 10 minutes
  (worked ok with 0m20s but not with 10m10s because the latter has greater length)

0.1.1 / 2020-05-19
==================

* Fix chunkify to work correctly with generators
* Small fix on timer tests

0.1.0 / 2020-05-19
==================

* Initial release with Timer and chunkify utilities
