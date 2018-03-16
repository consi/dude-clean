dude-cleaner.py - Dude database cleanup script
==============================================

Script removes all historical data from MikroTik Dude database. That includes:
* alerts
* graphs

Why this is needed?
-------------------
When your dude.db will reach 2.15GB it will simply stop working. This script will easy clean up database and give you some time to search other monitoring tool ;-)

How to use it?
--------------
```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
./dude-cleaner.py -s dude.db -d dude-fixed.db
```

And replace your dude.db in data/ directory of Dude Server installation. Also remove dude.db-journal and dude.viw before starting Dude server.

License
-------
The MIT License (MIT)

Copyright (c) 2018 Marek Wajdzik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Contact
-------
Marek Wajdzik <wajdzik.m@gmail.com>
