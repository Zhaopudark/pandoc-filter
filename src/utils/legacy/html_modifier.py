#!/usr/bin/env python
import panflute as pf
import re
import urllib.parse
import typeguard

import logging
import logging.handlers
import subprocess
from bs4 import BeautifulSoup
import hashlib


def main(file_name:str):
    with open(file_name, 'r+', encoding='utf-8') as file:
   
        soup = BeautifulSoup(file,features="html.parser")

        # 查找所有具有 class="footnote-ref" 的元素
        # **kwargs,关键字参数可以指定属性来搜索
        # https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/#keyword
        # class是python的关键字，所以用class_
        footnote_ref_elements = soup.find_all(
            name='a',
            string=re.compile(pattern=r"[\d]+"),
            class_='footnote-ref',
            href=re.compile(pattern=r"#fn[\d]+"),
            id=re.compile(pattern=r"fnref[\d]+"),
            role='doc-noteref'
            ) # [<a class="footnote-ref" href="#fn1" id="fnref1" role="doc-noteref"><sup>1</sup></a>,...]
        footnote_ref_dict = {}
        for item in footnote_ref_elements:
            fn_name1 = re.match(r"^#(fn[\d]+)",item.attrs['href']).groups()[0] # href="fnref1"
            fn_name2 = ''.join(re.match(r"^(fn)ref([\d]+)",item.attrs['id']).groups()) # id="fnref1"
            assert fn_name1 == fn_name2
            footnote_ref_dict[fn_name1] = item
        # print(footnote_ref_dict) 
        # {fn1': <a class="footnote-ref" href="#fn1" id="fnref1" role="doc-noteref"><sup>1</sup></a>,...}
        
        
        # 查找所有具有 class="footnote-back" 的元素, 以父级<li>元素为单位
        footnote_back_elements = soup.find_all(
            name='a',
            class_='footnote-back',
            href=re.compile(pattern=r"#fnref[\d]+"),
            role='doc-backlink') # [<a class="footnote-back" href="#fnref1" role="doc-backlink">↩︎</a>,...]
        footnote_back_li_elements = [item.find_parent('li',id=re.compile(pattern=r"fn[\d]*")) for item in footnote_back_elements]
        # [<li id="fn1"><p>https://zzz<a class="footnote-back" href="#fnref1" role="doc-backlink">↩︎</a></p></li>,...]
        
        footnote_back_dict = {}
        for item in footnote_back_li_elements:
            fn_name1 = re.match(r"^(fn[\d]+)",item.attrs['id']).groups()[0] #  id="fn1"
            fn_name2 = ''.join(re.match(r"^#(fn)ref([\d]+)",item.p.a.attrs['href']).groups()) # href="#fnref1"
            assert fn_name1 == fn_name2
            footnote_back_dict[fn_name1] = item
        # print(footnote_back_dict)
        # {'fn1': <li id="fn1"><p>https://zzz<a class="footnote-back" href="#fnref1" role="doc-backlink">↩︎</a></p></li>,...}
        
        
        ##  De-duplicate the footnote-back elements:
        # Group all footnote-back elements according to the footnote-back content.
        # In each group, merge all of the footnote-back elements into one, to realize the result like:
        # <li id="fn_name">
        #   <p>content
        #       <a class="footnote-back" href="#fn_name_1" role="doc-backlink">↩︎</a>
        #       <a class="footnote-back" href="#fn_name_2" role="doc-backlink">↩︎</a>
        #       <a class="footnote-back" href="#fn_name_3" role="doc-backlink">↩︎</a>
        #   </p></li>   
        # Modify the index (content|string) of the related footnote-ref elements simultaneously.
        non_duplication_fn_dict = {}
        fn_name_group_dict = {} 
        for fn_name,item in footnote_back_dict.items():
            hash_getter = hashlib.new('md5') # there is no need to use strong hash algorithm
            hash_getter.update(item.p.contents[0].encode('utf-8'))
            hash_value = hash_getter.hexdigest()
            if hash_getter.hexdigest() not in non_duplication_fn_dict:
                non_duplication_fn_dict[hash_value] = fn_name 
                fn_name_group_dict[fn_name] = [fn_name]
                # fn_merge_vector.append((fn_name,fn_name))
            else:
                # fn_merge_vector.append((fn_name,non_duplication_fn_dict[hash_value]))
                (fn_name_group_dict[non_duplication_fn_dict[hash_value]]).append(fn_name)
        # print(non_duplication_fn_dict)
        print(fn_name_group_dict)
        
        for global_index,(fn_name,fn_group) in enumerate(fn_name_group_dict.items()):
            _global_index = global_index+1
            for group_index,single_fn_name in enumerate(fn_group):
                if fn_name == single_fn_name:
                    assert group_index == 0
                    footnote_ref_dict[single_fn_name].sup.string = str(_global_index) 
                    footnote_ref_dict[single_fn_name].attrs['href'] = f"#fn{_global_index}"
                    footnote_ref_dict[single_fn_name].attrs['id'] = f"fnref{_global_index}"
                    footnote_back_dict[single_fn_name].p.a.attrs['href'] = f"#fnref{_global_index}"
                    footnote_back_dict[single_fn_name].p.a.attrs['id'] = f"fn{_global_index}"
                    # print(footnote_back_dict[single_fn_name].p.a.attrs['id'])
                    continue
                else:
                    _append_index = group_index
                    footnote_ref_dict[single_fn_name].sup.string = str(_global_index) 
                    # print(footnote_ref_dict[single_fn_name].sup.string)
                    footnote_ref_dict[single_fn_name].attrs['href'] = f"{footnote_ref_dict[fn_name].attrs['href']}-{_append_index}"
                    # print(footnote_ref_dict[single_fn_name].attrs['href'])
                    footnote_ref_dict[single_fn_name].attrs['id'] = f"{footnote_ref_dict[fn_name].attrs['id']}-{_append_index}"
                    # print(footnote_ref_dict[single_fn_name].attrs['id'])
                
                    
                    footnote_back_dict[single_fn_name].p.a.attrs['href'] = f"{footnote_back_dict[fn_name].p.a.attrs['href']}-{_append_index}"
                    # print(footnote_back_dict[single_fn_name].p.a.attrs['href'])
                    footnote_back_dict[single_fn_name].p.a.attrs['id'] = f"{footnote_back_dict[fn_name].p.a.attrs['id']}-{_append_index}"
                    # print(footnote_back_dict[single_fn_name].p.a.attrs['id'])
                    
                    footnote_back_dict[fn_name].p.append(footnote_back_dict[single_fn_name].p.a) # move and will delete the original one
                    footnote_back_dict[single_fn_name].extract() # extract from the tree (soup)
                    del footnote_back_dict[single_fn_name].attrs['id']
                    # (even though not delete from the memory directly, it will work as deletion if regenerate a new html from the modified tree)
            del footnote_back_dict[fn_name].attrs['id']      
        # print(footnote_ref_dict)
        # print(footnote_back_dict)

        file.seek(0)
        file.truncate() # clear all contents
        file.write(str(soup))
        # print("Modified HTML saved to 'modified.html'")

if __name__ == "__main__":
    
    import sys

    # 检查命令行参数是否包含文件名
    if len(sys.argv) != 2:
        print("Usage: python test.py <filename>")
        sys.exit(1)

    # 从命令行参数中获取文件名
    filename = sys.argv[1]
    # print(filename)
    try:
        
        main(filename)
    

    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
