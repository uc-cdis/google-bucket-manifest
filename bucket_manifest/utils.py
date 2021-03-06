import csv
from google.cloud import storage

import logging


def write_tsv(filename, files, fieldnames=None):
    """
    write to tsv file
    Args:
        filename(str): file name
        files(list(dict)): list of file info
        [
            {
                "GUID": "guid_example",
                "filename": "example",
                "size": 100,
                "acl": "['open']",
                "md5": "md5_hash",
            },
        ]
        fieldnames(list(str)): list of column names
    Returns:
        filename(str): file name
    """

    if not files:
        return None
    # Get column names
    fieldnames = fieldnames or files[0].keys()
    # Open tsv file
    with open(filename, mode="w") as outfile:
        writer = csv.DictWriter(outfile, delimiter="\t", fieldnames=fieldnames)
        # write header
        writer.writeheader()
        # Write data
        for f in files:
            for field in fieldnames:
                if field not in f:
                    f[field] = None
            writer.writerow(f)

    return filename


def upload_file(bucket_name, source_file_name, destination_blob_name):
    """
    Upload a file to an gs bucket
    
    Args:
        file_name: File to upload
        bucket: Bucket to upload to
        object_name: gs object name. If not specified then file_name is used
    Returns:
        Bool: True if file was uploaded, else False
    """
    # Initialize a storage client.
    storage_client = storage.Client()

    try:
        # Initialize a bucket client.
        bucket = storage_client.bucket(bucket_name)
        # Create a dest blob.
        blob = bucket.blob(destination_blob_name)
        # Upload file to the bucket
        blob.upload_from_filename(source_file_name)

    except Exception as e:
        logging.error(
            "Fail to upload {} to {}. Detail {}".format(
                source_file_name, bucket_name, e
            )
        )
        return False

    logging.info(
        "File {} uploaded to {}/{}.".format(source_file_name, bucket_name, destination_blob_name)
    )
    return True
