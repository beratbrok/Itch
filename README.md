# Itch
Creation of, parsing of, and limit-order-book construction from NASDAQ Itch Messages according to Genium INET® ITCH Protocol Specification for Borsa Istanbul (BIST). See http://www.borsaistanbul.com/docs/default-source/nasdaq-dokuman/bıstech-ıtch-protocol-specification.pdf for details.


See the unit tests in ITCH41Tests.py
* How to create an ITCH41 message from a list of user-friendly arguments, or from the raw bytes that one encounters in an actual NASDAQ ITCH 4.1 data feed for Borsa Istanbul (BIST).

* Itch41.py has the structs for all ITch message types and relevant member functions to parse them.
* parseItch.py - script that can take a raw message feed and run a custom function
* createItch.py - script that can take a list of user-friendly arguments and to create a binary file for testing your NASDAQ Itch 4.1 feed parser
* lob_bs.py defines the class lob_bs that constructs limit-order-book for the given ticker.
