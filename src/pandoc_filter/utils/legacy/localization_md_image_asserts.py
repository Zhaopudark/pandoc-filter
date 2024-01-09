#!/usr/bin/env python
import re
import sys
import os
import logging

import pathlib
import functools
import typeguard
import requests
from alive_progress import alive_bar

from ..logging_helper import logger_factory

script_file_name = os.path.basename(__file__)

logger = logger_factory(os.path.splitext(script_file_name)[0],logging.WARNING)

def get_normalized_src_alt_filepath(src:str,alt:str,img_save_dir:pathlib.Path):
    
    img_save_dir.mkdir(parents=True,exist_ok=True)
            
    file_extension = src.split('.')[-1]
    
    file_name = re.sub(r"[^\w\u4e00-\u9fa5]+", "-", alt) 
    file_name = file_name.strip('-')
    
    file_path = img_save_dir/f'{file_name}.{file_extension}'
    
    new_src = f"./{file_path.relative_to(img_save_dir.parent).as_posix()}"
    new_alt = file_name
    logger.info(f'new alt: {new_alt}')
    logger.info(f'new src: {new_src}')
    return new_src,new_alt,file_path   
    
    
def sub_html_img_pattern(match:re.Match,img_save_dir:str):
    group_dict = match.groupdict()
    src = group_dict['src']
    alt = group_dict['alt']
    style = group_dict['style']
    img_save_dir:pathlib.Path = pathlib.Path(img_save_dir)
    try:
        response = requests.get(src)
        if response.status_code == 200:
            # save local image
            # normlize file name -> normlize src and alt
            new_src,new_alt,file_path = get_normalized_src_alt_filepath(src,alt,img_save_dir)
            with open(file_path, 'wb') as img_file:
                img_file.write(response.content)
            return f'<img src="{new_src}" alt="{new_alt}" style="{style}"/>'
    except requests.exceptions.MissingSchema as e:
        # save local image
        # normlize file name -> normlize src and alt
        new_src,new_alt,file_path = get_normalized_src_alt_filepath(src,alt,img_save_dir)
        with open(img_save_dir.parent/src, 'rb') as img_file:
            content = img_file.read()
        with open(file_path, 'wb') as img_file:
            img_file.write(content)
        return f'<img src="{new_src}" alt="{new_alt}" style="{style}"/>'
    except Exception as e:
        logger.error(e)
        return f'<img src="{src}" alt="{alt}" style="{style}"/>'

def sub_markdown_img_pattern(match:re.Match,img_save_dir:str):
    group_dict = match.groupdict()
    src = group_dict['src']
    alt = group_dict['alt']
    img_save_dir:pathlib.Path = pathlib.Path(img_save_dir)
    try:
        response = requests.get(src)
        if response.status_code == 200:
            # save network image
            # normlize file name -> normlize src and alt
            new_src,new_alt,file_path = get_normalized_src_alt_filepath(src,alt,img_save_dir)
            with open(file_path, 'wb') as img_file:
                img_file.write(response.content)
            return f'![{new_alt}]({new_src})'
    except requests.exceptions.MissingSchema as e:
        # save local image
        # normlize file name -> normlize src and alt
        new_src,new_alt,file_path = get_normalized_src_alt_filepath(src,alt,img_save_dir)
        with open(img_save_dir.parent/src, 'rb') as img_file:
            content = img_file.read()
        with open(file_path, 'wb') as img_file:
            img_file.write(content)
        return f'![{new_alt}]({new_src})'
    except Exception as e:
        logger.error(e)
        return f'![{alt}]({src})'
    
def main(directory:str):
    """
    Localize all images of all markdown files in the directory. Specifically, the procedures are:
        1. Go through all markdown files in the directory.
        2. For each markdown file, specify an assets directory as `<markdown_file_name>.assets` in the same directory as the markdown file.
        3. Search the file content, find and save all image blocks:
            3.1 If the block is a html image block, get the `src`, `alt` and `style` attributes.
            3.2 If the block is a markdown image block, get the `src` and `alt` attributes.
            3.3 Normalize the `alt` attribute and use it as the image file name in next steps.
            3.4 If the image is a network image, download it and save it to the assets directory.
            3.5 If the image is a local image, copy it to the assets directory, ignore its original path.  If it is already in the assets directory, it will be refreshed.
        4. Modify the image blocks to match the changes above.
        5. Delete the assets directory if it is empty.
        6. Delete the image files in the assets directory if they are not used in the markdown file.
    Args:
        directory (str): the directory that contains all target markdown files
        
    """
    paths = pathlib.Path(directory).glob('**/*.md', case_sensitive=None)
    html_img_pattern = r"<img\s*(?:src=[\"\'](?P<src>[^\"\']*)[\"\'])?\s*(?:alt=[\"\'](?P<alt>[^\"\']*)[\"\']\s*)?(?:style=[\"\'](?P<style>[^\"\']*)[\"\'])?\s*/>"
    markdown_img_pattern = r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^\n\r]*)\)"
    paths:list[pathlib.Path] = list(paths)
    with alive_bar(len(paths)) as bar:
        for path in paths:

            assets_dir = path.parent / f'{path.stem}.assets'
            bar()
            with open(path, "r+", encoding="utf-8") as file:
                markdown_content = file.read()
              
                _sub_html_img_pattern = functools.partial(sub_html_img_pattern,img_save_dir=assets_dir)
                _sub_markdown_img_pattern = functools.partial(sub_markdown_img_pattern,img_save_dir=assets_dir)
                markdown_content = re.sub(html_img_pattern, _sub_html_img_pattern, markdown_content)
                markdown_content = re.sub(markdown_img_pattern, _sub_markdown_img_pattern, markdown_content)
                image_paths = []
                for item in re.findall(html_img_pattern, markdown_content):
                    image_paths.append(path.parent/item[0])
                for item in re.findall(markdown_img_pattern, markdown_content):
                    image_paths.append(path.parent/item[1])
                for item in image_paths:
                    if not item.exists():
                        logger.error(f"image not exists: {path}")
                        logger.error(f"image not exists: {item}")
                file.seek(0)
                file.truncate() # clear all contents
                file.write(markdown_content)
            if not assets_dir.exists():
                continue
            elif not any(assets_dir.iterdir()):
                assets_dir.rmdir()
                logger.warning(f"目录 '{assets_dir}' 已删除")   
            else:
                existent_image_paths = list(assets_dir.glob('*.*'))
                for item in existent_image_paths:
                    # logger.info(f"图片 '{item}'")
                    if item not in image_paths:
                        item.unlink()
                        logger.warning(f"图片 '{item}' 已删除")
            
            # if not any(assets_dir.iterdir()):
            #     print(f"目录 '{assets_dir}' 已删除")
            
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {script_file_name} <filename>")
        sys.exit(1)

    # 从命令行参数中获取文件名
    directory = sys.argv[1]
    try:
        main(directory=directory)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
   