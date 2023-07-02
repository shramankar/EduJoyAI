import os 
import re 

def next_story_directory(base_dir: str, name: str, create: bool = True):
    if not os.path.exists(base_dir):
        print(f"The directory {base_dir} does not exist.")
        return
    dirs = os.listdir(base_dir)
    story_dirs = [d for d in dirs if re.match(rf'{name}\d+', d)]
    if not story_dirs and create:
        new_dir = os.path.join(base_dir, name + '1')
        os.mkdir(new_dir)
        print(f"Created directory '{new_dir}'")
        return new_dir, 1
    story_numbers = [int(re.findall(r'\d+', d)[0]) for d in story_dirs]
    max_number = max(story_numbers)
    new_dir = os.path.join(base_dir, f'{name}{max_number + 1}')
    os.mkdir(new_dir)
    print(f"Created directory '{new_dir}'")
    return new_dir, max_number 