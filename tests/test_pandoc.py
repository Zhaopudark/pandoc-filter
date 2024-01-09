import pandoc_filter

def test_check_pandoc_version():
    pandoc_filter.pandoc_checker.check_pandoc_version('3.1.0')