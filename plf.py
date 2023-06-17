import psutil
import time
import argparse
import csv
import json
import xml.etree.ElementTree as ET


PROCESS_FIELDS = ['name', 'exe', 'create_time']
PROCESS_PARENT_FIELDS = ['name', 'exe']


def get_process_locations():
    process_locations = []
    for proc in psutil.process_iter(PROCESS_FIELDS):
        try:
            process_name = proc.info['name']
            process_exe = proc.info['exe']
            create_time = proc.info['create_time']
            parent_proc = proc.parent()  # get the parent process
            if parent_proc:  # check if the parent process exists
                parent_name = parent_proc.name()  # get the parent name
                parent_exe = parent_proc.exe()  # get the parent exe
            else:  # if there is no parent process, use None values
                parent_name = None
                parent_exe = None
            process_locations.append({
                'name': process_name,
                'exe': process_exe,
                'create_time': create_time,
                'parent': {
                    'name': parent_name,
                    'exe': parent_exe
                }
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_locations


def save_process_locations_to_csv(file_path, process_locations):
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
                                'Name', 'Executable', 'Creation Time', 'Parent Name', 'Parent Executable'])
        writer.writeheader()
        for process in process_locations:
            writer.writerow({
                'Name': process['name'],
                'Executable': process['exe'],
                'Creation Time': time.ctime(process['create_time']),
                'Parent Name': process['parent']['name'],
                'Parent Executable': process['parent']['exe']
            })


def save_process_locations_to_json(file_path, process_locations):
    with open(file_path, 'w') as file:
        json.dump(process_locations, file, indent=4)


def save_process_locations_to_xml(file_path, process_locations):
    root = ET.Element('Processes')
    for process in process_locations:
        proc_elem = ET.SubElement(root, 'Process')
        name_elem = ET.SubElement(proc_elem, 'Name')
        name_elem.text = process['name']
        exe_elem = ET.SubElement(proc_elem, 'Executable')
        exe_elem.text = process['exe']
        create_time_elem = ET.SubElement(proc_elem, 'CreationTime')
        create_time_elem.text = time.ctime(process['create_time'])
        parent_elem = ET.SubElement(proc_elem, 'Parent')
        parent_name_elem = ET.SubElement(parent_elem, 'Name')
        parent_name_elem.text = process['parent']['name']
        parent_exe_elem = ET.SubElement(parent_elem, 'Executable')
        parent_exe_elem.text = process['parent']['exe']

    tree = ET.ElementTree(root)
    tree.write(file_path, encoding='utf-8', xml_declaration=True)


def main(output_folder, format, interval, total_time):
    start_time = time.time()
    end_time = start_time + total_time

    process_locations = []
    while time.time() < end_time:
        process_locations.extend(get_process_locations())
        time.sleep(interval)

    if format == 'csv':
        file_path = f"{output_folder}/running_processes.csv"
        save_process_locations_to_csv(file_path, process_locations)
    elif format == 'json':
        file_path = f"{output_folder}/running_processes.json"
        save_process_locations_to_json(file_path, process_locations)
    elif format == 'xml':
        file_path = f"{output_folder}/running_processes.xml"
        save_process_locations_to_xml(file_path, process_locations)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Location Finder')
    parser.add_argument('-o', '--output', default='.', help='Output folder')
    parser.add_argument(
        '-f', '--format', choices=['csv', 'json', 'xml'], default='csv', help='Output format')
    parser.add_argument('-t', '--interval', type=int,
                        default=60, help='Time interval in seconds')
    parser.add_argument('-T', '--total-time', type=int,
                        default=600, help='Total time in seconds')

    args = parser.parse_args()
    main(args.output, args.format, args.interval, args.total_time)
