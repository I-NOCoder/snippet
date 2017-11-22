# -*- coding: utf-8 -*-


def str_timestamp(timestamp):
    return str(timestamp).rsplit(' ')[0]


def summary_length(summary, length):
    return summary[0: length]


filters = [
    str_timestamp,
    summary_length
]
