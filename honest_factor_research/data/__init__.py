"""Data loading + universe management for honest-factor-research.

Two main modules:

* :mod:`.fetch` — download OHLCV from yfinance + constituents from NASDAQ-screener
* :mod:`.snapshot` — long-format parquet I/O for frozen datasets
"""
