#!/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu May 29 09:09:14 2019
@author: skondaveeti
"""
import json
import datetime
import os
import sys
import argparse


class unbabel_cli:

    def __init__(self):
        self.json_file = None
        self.ws = None

    def is_valid_file(self, parser, arg):
        """
            Validate the input file
                params :
                    parser : ArgumentParser Handle ==> ArgumentParser
                    arg : string ==> Input file name.
                return :
                    an open file handle
        """
        if not os.path.exists(arg):
            parser.error("The file %s does not exist!" % arg)
        else:
            return open(arg, 'r')  # return an open file handle

    def validate_event(self, event):
        """
            validate event having the below mandatory keys:
                - duration
                - event_name and is set to translation_delivered
                - timestamp
            params:
                event : dict
            return :
                True/False
        """
        required = ['event_name', 'duration', 'timestamp']
        for elt in required:
            if elt not in event.keys():
                return False
            if event['event_name'] != 'translation_delivered':
                return False
        return True

    def validate_on_win_size(self, date, event_date, window_size=10):
        """
            validate the event on basis of Window Size.
            params:
                date : current date
                event_date : date from the list of events
            return :
                True/False
                True : if difference between date and event_date is <= window_size
                False : if not
        """
        window_size_delta = datetime.timedelta(minutes=window_size)
        if (date - event_date).days < 0:
            return False
        return (date - event_date) <= window_size_delta

    def compute_ma_time(self, events, frequency=1, window_size=10):
        """
            Count for each 'frequency' the average delivery time of 'events' for
            the past 'window_size' minutes
            params :
                events : list ==> sorted events list
                frequency : int ==> minutes
                window_size : int ==> last X minutes
            return :
                list of dict
        """
        cls_ub = unbabel_cli()
        frequency_delta = datetime.timedelta(minutes=frequency)
        start_time = datetime.datetime.strptime(events[0]['timestamp'], '%Y-%m-%d %H:%M:%S.%f').replace(second=0,
                                                                                                        microsecond=0)
        end_time = datetime.datetime.strptime(events[len(events) - 1]['timestamp'], '%Y-%m-%d %H:%M:%S.%f').replace(
            second=0, microsecond=0) + frequency_delta
        date = start_time
        data = []
        while date <= end_time:
            N = 0
            cum_sum = 0
            for idx, event in enumerate(events, 1):
                if not cls_ub.validate_event(event):
                    raise unbabel_cli_error('%s is not a valid event entry' % event)
                event_date = datetime.datetime.strptime(event['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
                if cls_ub.validate_on_win_size(date, event_date, window_size):
                    N += 1
                    cum_sum += event['duration']
            if N:
                data.append({'date': str(date), 'average_delivery_time': cum_sum / float(N)})
            else:
                data.append({'date': str(date), 'average_delivery_time': 0})
            date += frequency_delta
        # Writes the output to output.txt file
        f = open("output.txt", "w+")
        for i in range(len(data)):
            f.write(str(data[i]) + "\n")
        # Writes the output to data.json, if needed in JSON Format.
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)

    def exit_requirement_error(self):
        """
            Utility function to display on requirement mismatch error.
        """
        requirement_error = """Requirements :: 
                   must run on python 3.6
                   Execution Format ::
                   unbabel_cli --input_file (filename) --window_size (timeframe)
                   filename and timeframe are required
                   timeframe must be an integer
                   use --help to print this message
        """
        print(requirement_error)
        sys.exit(2)

    def main_func(self, args):
        """
            Main Function which loads the event data, sort the data and compute the moving average time and writes to
            data.json
            params :
                args : ArgumentParser Handle ==> Parsed input arguments.
        """
        # Get data and add it to the running counter
        self.json_file = args.input_file.name
        self.ws = args.window_size
        if not os.path.isfile(self.json_file):
            raise unbabel_cli_error('File Does not exist')
        events = [json.loads(line) for line in open(self.json_file, 'r')]
        events = sorted(events, key=lambda k: datetime.datetime.strptime(k['timestamp'], '%Y-%m-%d %H:%M:%S.%f'))
        cl_unbabel.compute_ma_time(events, window_size=self.ws)


class unbabel_cli_error(Exception):
    pass


if __name__ == '__main__':
    # Get arguments from the command line
    cl_unbabel = unbabel_cli()
    try:
        parser = argparse.ArgumentParser(
            description='command line application that parses a stream of events and produces an aggregated output.')
        parser.add_argument('--input_file', type=lambda x: cl_unbabel.is_valid_file(parser, x), required=True,
                            help='event log file Path {Ex:: events.json}')
        parser.add_argument('--window_size', type=int, required=True,
                            help='number representing window size (in minutes)')
        args = parser.parse_args()
        cl_unbabel.main_func(args)
    except:
        cl_unbabel.exit_requirement_error()
