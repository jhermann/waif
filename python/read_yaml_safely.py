"""
    Read a YAML file or stream safely.
"""

from pathlib import Path

def read_yaml_safely(filelike):
    """ Read a YAML file or stream with no RCE backdoors open (using the ‘safe’ loader).

        ``filelike`` can be a path or an open handle (supporting ``read()``).

        Supports a fallback chain of parsers as follows:
        PyYAML (C), PyYAML (Python), poyo, strictyaml.
    """
    # https://github.com/anthonywritescode/wat-02-pyyaml/blob/master/slides.md
    try:
        from yaml.cyaml import CSafeLoader as SafeYamlLoader
    except ImportError:
        try:
            from yaml import SafeLoader as SafeYamlLoader
        except ImportError:
            SafeYamlLoader = None

    if SafeYamlLoader:
        from yaml import load as yaml_load
        yaml_parser = lambda stream: yaml_load(stream, Loader=SafeYamlLoader)
    else:
        try:
            import poyo  # poyo is optional! # pylint: disable=import-error
        except ImportError:
            try:
                import strictyaml  # strictyaml is optional! # pylint: disable=import-error
            except ImportError:
                raise RuntimeError("Please 'pip install' one of PyYAML, poyo, or strictyaml.")
            else:
                yaml_parser = strictyaml.load
        else:
            yaml_parser = poyo.parse_string

    try:
        yaml_text = filelike.read()
    except AttributeError:
        with Path(filelike).open('rb') as handle:
            yaml_text = handle.read()

    if not isinstance(yaml_text, str):
        try:
            yaml_text = yaml_text.decode('utf-8')
        except UnicodeError:
            yaml_text = yaml_text.decode('iso-8859-1')

    try:
        return yaml_parser(yaml_text)
    except Exception as cause:
        raise RuntimeError(str(cause)) from cause


if __name__ == '__main__':
    from io import StringIO
    from pprint import pprint

    pprint(read_yaml_safely(StringIO('list: [1,2,3]')))
