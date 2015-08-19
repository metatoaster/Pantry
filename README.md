# Pantry

A simple context manager based file store that uses the pickle module

Use:
```python
from Pantry import pantry

shelves = {'first': ['cereal', 'rice', 'beans'],
           'second': ['spam', 'spam', 'baked beans', 'spam']}

with pantry('pantry.txt') as db:
    db['shelves'] = shelves

