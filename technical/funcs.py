from technical.settings import DEBUG


def dprint(*args, **kwargs):
    if DEBUG:
        print('dprint() > ', *args, **kwargs)
