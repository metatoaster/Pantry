from pantry import pantry
from random import randint
from datetime import datetime
from datetime import timedelta

def magic_api(word):
    """
    This is our magic API that we're simulating.
    It'll return a random number and a cache timer.

    """
    result = sum(ord(x)-65 + randint(1,50) for x in word)
    delta = timedelta(seconds=result)
    cached_until = datetime.now() + delta
    return result, cached_until

def on_first_run():
    # list of four letter Q words... because.
    wordbank =  'QAID QATS QINS QOPH QUAD QUAG QUAI QUAT QUAY '
    wordbank += 'QUEP QUEY QUID QUIM QUIN QUIP QUIT QUIZ QUOD QUOP'
    schema = ('result', 'cached_until')

    # setting up our pantry
    with pantry('demo.pk') as db:
        for word in wordbank.split():
            api_result = magic_api(word)
            db[word] = dict(zip(schema, api_result))

def update():

    with pantry('demo.pk') as db:
        for k, v in sorted(db.items(), key=lambda x: x[1]['cached_until']):
            if v['cached_until'] < datetime.now():
                print('{} is being updated'.format(k))
                result, cached_until = magic_api(k)
                v['result'] = result
                v['cached_until'] = cached_until
            else:
                time_left = (v['cached_until'] - datetime.now()).seconds
                print('{} has {} seconds until it needs updated'.format(k, time_left))


if __name__ == "__main__":
    update()
