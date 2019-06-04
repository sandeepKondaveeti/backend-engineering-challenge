# Moving average Solution #

Hey Unbabel Team!

**Environment Specification:#

The machine should have python3 installed and have the json and argparse dependencies installed.

**Executing the code:**

Navigate to the repository folder and execute the below line of code in the command prompt.
```python unbabel_cli.py --input_file <input json file> --window_size <window size in minutes>```

For usage help, run python **unbabel_cli.py --help**

** Code
Problem given is a typical sliding window problem. Solution is built around event streams, meaning
that it should always be processing data and output its results in real-time as well.
To achieve this, the program can take its input from a regular file

Unpacking the functions provided in unbabel_cli.py file:

is_valid_file -- Validates the input file. 

validate_event -- Validates event having the below mandatory keys.

validate_on_win_size -- Validates the event on basis of Window Size.

compute_ma_time -- Count for each 'frequency' the average delivery time of 'events' for the past 'window_size' minutes

exit_requirement_error -- Utility function to display on requirement mismatch error.

main_func -- Main Function which loads the event data, sort the data and compute the moving average time and writes to
            data.json and output.txt.

**Challenge Objective:**

Your mission is to build a simple command line application that parses a stream of events and produces an aggregated output. In this case, we're interested in calculating, for every minute, a moving average of the translation delivery time for the last X minutes.

If we want to count, for each minute, the moving average delivery time of all translations for the past 10 minutes we would call your application like (feel free to name it anything you like!).

**unbabel_cli --input_file events.json --window_size 10**

The input file format would be something like:

```
{"timestamp": "2018-12-26 18:11:08.509654","translation_id": "5aa5b2f39f7254a75aa5","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 20}
{"timestamp": "2018-12-26 18:15:19.903159","translation_id": "5aa5b2f39f7254a75aa4","source_language": "en","target_language": "fr","client_name": "easyjet","event_name": "translation_delivered","nr_words": 30, "duration": 31}
{"timestamp": "2018-12-26 18:23:19.903159","translation_id": "5aa5b2f39f7254a75bb33","source_language": "en","target_language": "fr","client_name": "booking","event_name": "translation_delivered","nr_words": 100, "duration": 54}
```

The output file would be something in the following format.
```
{"date": "2018-12-26 18:11:00", "average_delivery_time": 0}
{"date": "2018-12-26 18:12:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:13:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:14:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:15:00", "average_delivery_time": 20}
{"date": "2018-12-26 18:16:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:17:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:18:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:19:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:20:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:21:00", "average_delivery_time": 25.5}
{"date": "2018-12-26 18:22:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:23:00", "average_delivery_time": 31}
{"date": "2018-12-26 18:24:00", "average_delivery_time": 42.5}
```
**Output::**

Output is stored in data.json which is in JSON Format and output.txt contains the given output format.
