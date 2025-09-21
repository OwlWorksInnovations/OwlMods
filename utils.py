import os, shutil, filecmp

def get_files_in_dir(path: str):
    files_list: list = []

    for root, _, files in os.walk(path):
        for file in files:
            files_list.append(os.path.join(root, file))

    return files_list

def backup_files_dir(source: str, destination: str):
    os.makedirs(destination, exist_ok=True)
    for root, _, files in os.walk(source):
        relative: str = os.path.relpath(root, source)
        destination_dir: str = os.path.join(destination, relative)
        os.makedirs(destination_dir, exist_ok=True)

        for file in files:
            s: str = os.path.join(root, file)
            d: str = os.path.join(destination_dir, file)
            if not os.path.exists(d) or not filecmp.cmp(s, d, shallow=False):
                shutil.copy2(s, d)

    dir_size_bytes: int = check_dir_size(destination)
    dir_size_kb = dir_size_bytes / 1024
    dir_size_mb = dir_size_kb / 1024
    dir_size_gb = dir_size_mb / 1024

    if dir_size_gb >= 1:
        print(f"File size is quite large: {dir_size_gb:.2f}GB")
    else:
        print(f"File size is: {dir_size_mb:.2f}MB")

def backup_file(source: str, destination: str, filename: str):
    os.makedirs(destination, exist_ok=True)
    file = os.path.join(source, filename)
    shutil.copy2(file, destination)

def check_dir_size(path: str):
    files: list = get_files_in_dir(path)

    size = 0
    for file in files:
        size += os.path.getsize(file)

    return size

def delete_file(path:str, filename: str):
    file = os.path.join(path, filename)
    os.remove(file)
    print(f"File has been removed: {filename}")