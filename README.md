# pymonero

A python tool for Monero. See `LICENSE` for use.

## Features

* bitmonerod daemon RPC communication
* simplewallet RPC communication
* Payment ID generator
* More Soon&trade;

## Requirements

Pymonero has been tested on Python 2.7.11 and 3.5.1. It may or may not work in other versions.

### Non-Standard Packages

Pymonero primarily uses the Standard Python Library, but we are open to using other packages
when doing so reduces developer maintenance and improves our code. Currently, pymonero uses:

* requests - [http://python-requests.org](http://python-requests.org)

## Usage

See `example-bitmonero.py` for example script showcasing daemon methods.

Documentation is available in this repository's [wiki](https://github.com/Monero-Monitor/pymonero/wiki) page.

## Unit Tests

Unit tests are always being expanded and improved. Current tests can be found in `tests`.

As an example, to run tests for connecting with the daemon, `python test-bitmonerod.py`.

## Acknowledgements

Some initial code inspired by [Monero Examples](https://moneroexamples.github.io/python-json-rpc/).
In particular, those examples were helpful in extracting block and block header information from
the somewhat clunky form that it is returned by their respective json_rpc calls.
