from ..constants.versioned_document import MetaSectionKey, IdentifierDelimeter


def deconstruct_identifier(identifier):
    domain, remainder = identifier.split(IdentifierDelimeter.DOMAIN)
    name, version = remainder.split(IdentifierDelimeter.VERSION)
    return {
        MetaSectionKey.DOMAIN: domain,
        MetaSectionKey.NAME: name,
        MetaSectionKey.VERSION: version
    }


def construct_identifier(meta_values):
    return '{domain}{domain_delim}{method}{version_delim}{version}'.format(
        domain=meta_values[MetaSectionKey.DOMAIN],
        domain_delim=IdentifierDelimeter.DOMAIN,
        method=meta_values[MetaSectionKey.NAME],
        version_delim=IdentifierDelimeter.VERSION,
        version=str(meta_values[MetaSectionKey.VERSION]),
    )


def path_for_identifier(identifier, root_path=None):
    root_path = root_path  # todo: thing_that_loads_config_file_and_gets_default_root_path()
    meta_info = deconstruct_identifier(identifier)
    return '{root_path}/{domain}/{name}/{version}.yaml'.format(
        root_path=root_path,
        domain=meta_info[MetaSectionKey.DOMAIN],
        name=meta_info[MetaSectionKey.NAME],
        version=meta_info[MetaSectionKey.VERSION].replace('.', '_')
    )