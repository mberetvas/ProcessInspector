```
# Process Location Finder (PLF)

PLF is a script written in Python that retrieves information about running processes on a system, including their names, locations, and parent processes. It provides the ability to save this information in different formats such as CSV, JSON, and XML.

## Prerequisites

- Python 3.x
- psutil library (`pip install psutil`)

## Usage

```shell
python plf.py -o <output_folder> -f <format>
```

- `-o <output_folder>` (optional): Specify the output folder where the result file will be saved. If not provided, the file will be saved in the current directory.
- `-f <format>`: Specify the output format. Choose one of the following options: `csv`, `json`, or `xml`.

Example:
```shell
python plf.py -o /path/to/output/folder -f json
```

The script will retrieve the running process information and save it as a JSON file in the specified output folder.

## Output

The script generates a file named `running_process_locations.<format>` in the specified output folder. The format can be `csv`, `json`, or `xml`, depending on the chosen format.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

PLF uses the `psutil` library for retrieving process information. More information about `psutil` can be found [here](https://github.com/giampaolo/psutil).

```

Make sure to include a `LICENSE` file in your repository containing the license text for your project.

Feel free to modify the README file according to your specific needs and add any additional sections or information you think is relevant.