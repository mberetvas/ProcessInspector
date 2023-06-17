import psutil


def get_process_locations():
    process_locations = []
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            process_name = proc.info['name']
            process_exe = proc.info['exe']
            process_locations.append(f"{process_name}: {process_exe}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_locations


def save_process_locations_to_file(file_path):
    process_locations = get_process_locations()
    with open(file_path, 'w') as file:
        file.write('\n'.join(process_locations))


# Usage example
save_process_locations_to_file('running_process_locations.txt')
