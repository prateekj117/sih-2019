import os
import glob

def get_excel(folder_name, default_file=False):
    files = glob.glob("data/uploads/{}/*.xlsx".format(folder_name))
    if len(files) == 0:
        return default_file
    times = []
    for file in files:
        times.append(int(os.path.getmtime(file)))

    max_time = max(times)
    for (idx, time) in enumerate(times):
        if time == max_time:
            break
    return files[idx]
