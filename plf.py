import sys
import os
import csv
import json
import xml.etree.ElementTree as ET
import psutil
import argparse


def get_process_locations():
    process_locations = []
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            process_name = proc.info['name']
            process_exe = proc.info['exe']
            parent_proc = proc.parent()  # get the parent process
            if parent_proc:  # check if the parent process exists
                parent_name = parent_proc.name()  # get the parent name
                parent_exe = parent_proc.exe()  # get the parent exe
            else:  # if there is no parent process, use None values
                parent_name = None
                parent_exe = None
            process_locations.append({
                'Process Name': process_name,
                'Process Location': process_exe,
                'Parent Name': parent_name,
                'Parent Location': parent_exe
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_locations


def save_process_locations(file_path, output_format):
    process_locations = get_process_locations()
    if output_format == 'csv':
        save_as_csv(file_path, process_locations)
    elif output_format == 'json':
        save_as_json(file_path, process_locations)
    elif output_format == 'xml':
        save_as_xml(file_path, process_locations)
    else:
        print("Invalid output format. Please choose 'csv', 'json', or 'xml'.")


def save_as_csv(file_path, process_locations):
    fieldnames = ['Process Name', 'Process Location',
                  'Parent Name', 'Parent Location']
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(process_locations)


def save_as_json(file_path, process_locations):
    with open(file_path, 'w') as file:
        json.dump(process_locations, file, indent=4)


def save_as_xml(file_path, process_locations):
    root = ET.Element('Processes')
    for process in process_locations:
        process_elem = ET.SubElement(root, 'Process')
        for key, value in process.items():
            attr_elem = ET.SubElement(process_elem, key.replace(' ', '_'))
            attr_elem.text = str(value)
    tree = ET.ElementTree(root)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog='plf.py', description='Process Location Finder')
    parser.add_argument('-o', '--output-folder',
                        metavar='<output_folder>', help='Specify the output folder')
    parser.add_argument('-f', '--format', metavar='<format>',
                        help="Specify the output format: 'csv', 'json', or 'xml'")
    return parser.parse_args()


def print_help(parser):
    parser.print_help()


# Usage example
args = parse_arguments()

if args.format:
    output_format = args.format.lower()
    if output_format not in ['csv', 'json', 'xml']:
        print("Invalid output format. Please choose 'csv', 'json', or 'xml'.")
        sys.exit(1)
else:
    print("Output format is required. Please specify 'csv', 'json', or 'xml'.")
    sys.exit(1)

output_folder = args.output_folder if args.output_folder else os.getcwd()
file_name = f'running_process_locations.{output_format}'
file_path = os.path.join(output_folder, file_name)
save_process_locations(file_path, output_format)
