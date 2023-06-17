# Process Location Finder (PLF)

PLF is a script written in Python that retrieves information about running processes on a system, including their names, locations, parent processes, and activation time. It provides the ability to save this information in different formats such as CSV, JSON, and XML. It also allows continuous monitoring of new processes over a specified time interval.

## Prerequisites

- Python 3.x
- psutil library (`pip install psutil`)

## Usage

```shell
python plf.py -o <output_folder> -f <format> -t <interval> -T <total_time>
```

- `-o <output_folder>` (optional): Specify the output folder where the result file will be saved. If not provided, the file will be saved in the current directory.
- `-f <format>`: Specify the output format. Choose one of the following options: `csv`, `json`, or `xml`.
- `-t <interval>`: Specify the time interval in seconds at which the process list should be updated. This determines how frequently new processes are checked.
- `-T <total_time>`: Specify the total duration in seconds for which the script should monitor new processes and update the list.

Example:
```shell
python plf.py -o /path/to/output/folder -f json -t 60 -T 600
```

The script will continuously monitor the running processes, update the process list every 60 seconds, run for 600 seconds (10 minutes), and save the final process locations as a JSON file in the specified output folder.

## Output

The script generates a file named `running_process_locations.<format>` in the specified output folder. The format can be `csv`, `json`, or `xml`, depending on the chosen format. The file contains information about the running processes, including their names, locations, parent processes, and activation time.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

PLF uses the `psutil` library for retrieving process information. More information about `psutil` can be found [here](https://github.com/giampaolo/psutil).