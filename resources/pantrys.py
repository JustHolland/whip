import models

from flask import Blueprint



pantrys= Blueprint('pantry', 'pantrys')

@pantrys.route('/')
def pantrys_index():
    return "pantry is working"
