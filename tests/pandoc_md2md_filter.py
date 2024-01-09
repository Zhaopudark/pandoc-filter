#!/usr/bin/env python
import pathlib
import logging
import functools
import datetime
import typeguard
import zlib
import panflute as pf
from pandoc_filters.utils.logging_helper import TracingLogger,logger_factory
from pandoc_filters.utils.oss_helper import OssHelper
from pandoc_filters.pandoc_checker import check_pandoc_version
from pandoc_filters.md2md_filters import math_filter,figure_filter,footnote_filter,internal_link_filter


@typeguard.typechecked
def finalize(doc:pf.Doc,**kwargs):
    # metadata_dict =  doc.get_metadata() # See http://scorreia.com/software/panflute/code.html#:~:text=add%20attributes%20freely-,get_metadata,-(%5Bkey
    # metadata_dict['date'] = datetime.datetime.fromtimestamp(doc.doc_path.stat().st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    # metadata_dict['updated'] = datetime.datetime.fromtimestamp(doc.doc_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    # # meda_data['inno'] = doc_path.stat().st_ino
    # metadata_dict['abbrlink'] = hex(zlib.crc32(bytes(metadata_dict.get('title','').encode('utf-8'))))[2::]
    # current_abbrlink = metadata_dict['abbrlink']
    # global_abbrlink_file_recoder = kwargs['global_abbrlink_file_recoder']
    # if current_abbrlink in global_abbrlink_file_recoder:
    #     raise Exception(f"The abbrlink `{current_abbrlink}` has already been used for file {global_abbrlink_file_recoder[current_abbrlink]}, but the file {doc.doc_path} also want to use the same abbrlink.")
    # else:
    #     global_abbrlink_file_recoder[current_abbrlink] = doc.doc_path
    # doc.metadata = pf.MetaMap(**metadata_dict)
    if (doc.get_metadata(key='hide',default=False)):
        doc.metadata['sitemap'] = False
        
    doc.metadata['math'] = doc.have_math
    doc.metadata['date'] = datetime.datetime.fromtimestamp(doc.doc_path.stat().st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    doc.metadata['updated'] = datetime.datetime.fromtimestamp(doc.doc_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    current_abbrlink = hex(zlib.crc32(bytes(doc.get_metadata(key='title',default='').encode('utf-8'))))[2::] # eliminate the '0x' prefix
    global_abbrlink_file_recoder = kwargs['global_abbrlink_file_recoder']
    if current_abbrlink in global_abbrlink_file_recoder:
        raise Exception(f"The abbrlink `{current_abbrlink}` has already been used for file {global_abbrlink_file_recoder[current_abbrlink]}, but the file {doc.doc_path} also want to use the same abbrlink.")
    else:
        global_abbrlink_file_recoder[current_abbrlink] = doc.doc_path
        doc.metadata['abbrlink'] = current_abbrlink

def main(doc=None,**kwargs):
    check_pandoc_version(required_version='3.1.0')
    _finalize = functools.partial(finalize,**kwargs)
    return pf.run_filters(actions= [math_filter,figure_filter,footnote_filter,internal_link_filter],finalize=_finalize,doc=doc,**kwargs)


if __name__ == "__main__":
    
    import sys
    
    # 检查命令行参数是否包含文件名
    if len(sys.argv) != 3:
        print("Usage: python markdown_deployer.py <notes_dir> <target_dir>")
        sys.exit(1)
    print(sys.argv)
    
    notes_dir = sys.argv[1]
    target_dir = sys.argv[2]
    
    import os
    try:
        oss_endpoint_name = os.environ['OSS_ENDPOINT_NAME']
        oss_bucket_name = os.environ['OSS_BUCKET_NAME']
        assert os.environ['OSS_ACCESS_KEY_ID']
        assert os.environ['OSS_ACCESS_KEY_SECRET']
    except KeyError as e:
        print(f"Please set the environment variable {e}")
        sys.exit(1)
    
    oss_helper = OssHelper(oss_endpoint_name,oss_bucket_name)
    global_abbrlink_file_recoder = {}
    tracing_logger = TracingLogger(name='logs/pf_log',level=logging.WARNING)
    logger = logger_factory(name='logs/pf_log',level=logging.WARNING)
    for file_path in pathlib.Path(notes_dir).glob('**/*.md'):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                markdown_content = f.read()
            doc = pf.convert_text(markdown_content,input_format='markdown',output_format='panflute',standalone=True)
            if doc.get_metadata():
                doc.doc_path = file_path
                doc = main(doc,
                           oss_helper=oss_helper,
                           tracing_logger = tracing_logger,
                           global_abbrlink_file_recoder=global_abbrlink_file_recoder)
                with open(f"{target_dir}/{file_path.name}", "w", encoding="utf-8") as f:
                    f.write(pf.convert_text(doc,input_format='panflute',output_format='gfm',standalone=True))
        except Exception as e:
            logger.error(e)
        finally:
            f.close()
        