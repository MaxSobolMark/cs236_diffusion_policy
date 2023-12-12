'''
Script to filter demonstrations based on quality.
'''

import h5py
import random

def copy_group(src_group, dest_group):
    """Recursively copy contents from src_group to dest_group."""
    for name, item in src_group.items():
        if isinstance(item, h5py.Dataset):
            # Copy dataset
            dest_group.create_dataset(name, data=item[()])
        elif isinstance(item, h5py.Group):
            # Create a new group and copy its contents
            new_group = dest_group.create_group(name)
            copy_group(item, new_group)


def filter_demos(demo_path, output_path, mode="better"):
    """Filters demonstrations based on quality."""
    original_demos = h5py.File(demo_path, "r")
    new_demos = h5py.File(output_path, "w")

    # Copy over metadata
    mask_group = new_demos.create_group("mask")
    copy_group(original_demos["mask"], mask_group)

    # Select demonstrations
    if mode == "better":
        samples = original_demos["mask"]["better"][:]
    elif mode == "worse":
        samples = original_demos["mask"]["worse"][:]
    elif mode == "mix":
        worse_samples = original_demos["mask"]["worse"][:]
        better_samples = original_demos["mask"]["better"][:]

        worse_samples_str = [demo.decode('utf-8') for demo in worse_samples]
        better_samples_str = [demo.decode('utf-8') for demo in better_samples]

        sampled_worse = random.sample(worse_samples_str, 50)
        sampled_better = random.sample(better_samples_str, 50)

        samples = sampled_worse + sampled_better

    # Copy over demonstrations
    data_group = new_demos.create_group("data")
    for new_idx, demo_key in enumerate(samples):
        new_demo_group = data_group.create_group(f'demo_{new_idx}')
        copy_group(original_demos["data"][demo_key], new_demo_group)
    
    new_demos.close()

if __name__ == "__main__":
    demo_path = ... # Path to original mixed-human demonstrations
    output_path = ... # Path to save filtered demonstrations
    for mode in ["better", "worse", "mix"]:
        filter_demos(demo_path, output_path, mode=mode)