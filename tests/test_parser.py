#adding this later to fix pytest discovery

import  faultsift.parser as parser


def test_parser_module_imports() :
    assert parser is not None