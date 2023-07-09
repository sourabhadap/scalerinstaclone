from scalerinstaclone.celery import app


# TODO: EXPLORE LOGGING & DEBUGGING IN CELERY
@app.task(name='sum_two_numbers')
def add(x, y):
    return x + y
