import os
import shutil


def can_be_removed(directory: str) -> bool:
    """
    Checks if the specified directory can be removed.
    It is considered removable if all of its subdirectories are removable.

    Args:
        directory (str): The path to the directory to check.

    Returns:
        bool: True if the directory can be removed, False otherwise.

    Raises:
        ValueError: If the specified path is not a valid directory.
    """
    # Check if the specified path is a valid directory
    if not os.path.isdir(directory):
        raise ValueError(f"The specified path is not a valid directory: {directory}")

    try:
        # Iterate over the items in the directory
        for item in os.scandir(directory):
            # Check if the item is None (should not happen)
            if item is None:
                raise TypeError("os.scandir() returned None")

            # Ignore hidden files
            if item.name.startswith("."):
                continue

            # Check if the item is a directory
            if not item.is_dir():
                return False
            else:
                # Recursively check if the subdirectory can be removed
                if not can_be_removed(item.path):
                    return False
        return True
    except Exception as exc:
        # Print an error message if an exception occurs
        print(f"An error occurred while checking if '{directory}' can be removed: {exc}")
        return False


def remove_empty_folders(directory: str) -> None:
    """
    Removes empty folders from the specified directory and all of its subdirectories.

    This function iterates over the items in the directory and checks if each item is a directory.
    If it is a directory, it checks if it can be removed using the can_be_removed() function.
    If it can be removed, it prints a message and then removes the directory using shutil.rmtree().

    Args:
        directory (str): The path to the directory from which to remove empty folders.

    Returns:
        None
    """
    # Iterate over the items in the directory
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        # Check if the item is a directory
        if os.path.isdir(item_path):
            # Check if the directory can be removed
            if can_be_removed(item_path):
                # Print a message if it can be removed
                print(f"Can be removed folder: \033[92m{item_path}\033[0m")
                # Remove the directory using shutil.rmtree()
                shutil.rmtree(item_path)
    # Print a message after all empty folders have been removed
    print("\033[92mAll empty folders have been removed.\033[0m")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            remove_empty_folders(sys.argv[1])
        else:
            print(f"\033[91mError: '{sys.argv[1]}' is not a directory.\033[0m")
    else:
        remove_empty_folders(r"/share/incompleted/Driver")
