import sys
import csv
import json
import xml.etree.ElementTree as ET
import psutil


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


def print_help():
    print("")
    print("---------------Process Location Finder---------------")
    print("")
    print("Usage: python plf.py <output_file_path> <output_format>")
    print("Valid output formats: 'csv', 'json', 'xml'")
    print("")
    print("-----------------------------------------------------")
    print("")


# Usage examplels
if len(sys.argv) == 2 and sys.argv[1] == '--help':
    print_help()
elif len(sys.argv) != 3:
    print("Invalid number of arguments. Use '--help' for more information.")
else:
    file_path = sys.argv[1]
    output_format = sys.argv[2].lower()
    save_process_locations(file_path, output_format)
