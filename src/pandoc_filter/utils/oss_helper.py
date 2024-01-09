import hashlib
from typing import Literal
import pathlib
import shutil
import logging
from .logging_helper import logger_factory
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from oss2.models import BucketReferer

class OssHelper:
    
    def __init__(self,endpoint_name:str,bucket_name:str) -> None:
        self.logger = logger_factory('logs/oss_log',logging.INFO)
        # self.local_cache_dir = pathlib.Path(local_cache_dir)
        # self.local_relative_root = pathlib.Path(local_relative_root)
        # 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
        self.auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
        self.endpoint_name = endpoint_name
        self.bucket_name = bucket_name
        self.bucket = oss2.Bucket(self.auth,endpoint=self.endpoint_name,bucket_name=self.bucket_name)
        self.domain = self.bucket.list_bucket_cname().cname[0].domain
        
    def get_hashed_file_name(self,file_path:str,hash_algorithm:Literal['md5','sha1','sha256','sha512']):
        file_path = pathlib.Path(file_path)
        with open(file_path, 'rb') as file:
            file_data  = file.read()
        file_hash = hashlib.new(hash_algorithm)
        file_hash.update(file_data)
        return f"{file_hash.hexdigest()}{file_path.suffix}"
    def maybe_upload_file_and_get_src(self,file_path:str)->str:
        r"""Try to upload file to oss. Use hash to indentify all files.
            1. Read and calculate the hash of the input file.
            2. Then get a file name based on the hash.
            3. If the file name has not existed in the bucket, upload the file.
            4. Return the url of the file.
        """
        obj_name = self.get_hashed_file_name(file_path,'sha256')
        # local_file_path = self.local_cache_dir/obj_name
        # if local_file_path.exists():
        #     return '/'+str(local_file_path.relative_to(self.local_relative_root))
        # else:
        #     shutil.copy2(file_path, local_file_path)
        #     return '/'+str(local_file_path.relative_to(self.local_relative_root))
        
        if self.bucket.object_exists(obj_name):
            self.logger.info(f"The object {obj_name} has already existed.")
        else:
            self.bucket.put_object_from_file(obj_name, file_path)
            self.logger.info(f"The object {obj_name} has been uploaded.")
        return f"https://{self.domain}/{obj_name}"
    
if __name__ == "__main__":
    oss_helper = OssHelper(endpoint_name='oss-cn-nanjing.aliyuncs.com',bucket_name='raw-blog')
    print(oss_helper.domain)