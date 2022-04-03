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


def identifier_for_path(*args, **kwargs):
    msg = 'Not Implemented: identifier_for_path()' \
          'This is being left unimplemented as an affirmative design decision. ' \
          'Needing this function to exist should be considered a sign that you are on the Thorny Road to Sadness.' \
          'You are urged to reconsider the path that brought you here.'
    raise NotImplementedError(msg)
