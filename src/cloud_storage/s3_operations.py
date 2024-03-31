from src.exception import CustomException

import os
import sys


class S3Operation:
    """A class to perform synchronization operations between local folders and Amazon S3 buckets.

    This class provides methods to upload or download new or changed files between a local folder and
    a specified folder within an Amazon S3 bucket.

    Attributes:
        None

    Methods:
        sync_folder_to_s3: Syncs a local folder to a specified folder within an S3 bucket.
        sync_folder_from_s3: Syncs a specified folder within an S3 bucket to a local folder.
    """

    def sync_folder_to_s3(self,
                          folder: str,
                          bucket_name: str,
                          bucket_folder_name: str) -> None:
        """Syncs a specified folder within an S3 bucket to a local folder.

        Args:
            folder (str): The local folder path to sync to.
            bucket_name (str): The name of the S3 bucket.
            bucket_folder_name (str): The folder path within the S3 bucket to sync from.

        Returns:
            None

        Raises:
            CustomException: If there is an error during the sync operation.
        """

        try:
            command: str = (
                f"aws s3 sync {folder} s3://{bucket_name}/{bucket_folder_name} "
            )

            os.system(command)

        except Exception as e:
            raise CustomException(e, sys)

    def sync_folder_from_s3(self,
                            folder: str,
                            bucket_name: str,
                            bucket_folder_name: str) -> None:
        """Syncs a specified folder within an S3 bucket to a local folder.

        Args:
            folder (str): The local folder path to sync to.
            bucket_name (str): The name of the S3 bucket.
            bucket_folder_name (str): The folder path within the S3 bucket to sync from.

        Returns:
            None

        Raises:
            CustomException: If there is an error during the sync operation.
        """
        try:
            ''' It was not working
            command: str = (
                f"aws s3 sync s3://{bucket_name}/{bucket_folder_name}/ {folder} "
            )
            '''
            command: str = (
                f"aws s3 cp s3://{bucket_name}/{bucket_folder_name} {folder} "
            )

            os.system(command)

        except Exception as e:
            raise CustomException(e, sys)
