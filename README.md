# Remaining-Time-To-Process (RTPT)
[![PyPI version](https://badge.fury.io/py/rtpt.svg)](https://badge.fury.io/py/rtpt)

RTPT class to rename your processes giving information on who is launching the process, and the remaining time for it.

# Installation
## Using pip

	pip install rtpt

# From source

	git clone
	python setup.py install


## Example

.. code:: python
```python
from rtpt.rtpt import RTPT
import random
import time

# Create RTPT object
rtpt = RTPT(name_initials='QD', experiment_name='TestingRTPT', max_iterations=10)

# Start the RTPT tracking
rtpt.start()

# Loop over all iterations
for epoch in range(10):
    time.sleep(4)
    # Perform a single experiment iteration
    loss = random.random()

    # Update the RTPT (subtitle is optional)
    rtpt.step(subtitle=f"loss={loss:2.2f}")
```
