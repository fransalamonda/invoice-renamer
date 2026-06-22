import os
import shutil


def move_and_rename(
    source_file,
    output_folder,
    company_name,
    new_filename
):

    company_folder = os.path.join(
        output_folder,
        company_name
    )

    os.makedirs(
        company_folder,
        exist_ok=True
    )

    destination = os.path.join(
        company_folder,
        new_filename
    )

    shutil.move(
        source_file,
        destination
    )

    return destination