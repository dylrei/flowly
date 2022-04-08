from ..constants.identity import IdentityDelimeter, MetaSectionKey
from ..constants.runtime import IdentityConfigsKey
from ..runtime import IdentityConfigs


def deconstruct_identity(identity):
    domain, remainder = identity.split(IdentityDelimeter.DOMAIN)
    name, version = remainder.split(IdentityDelimeter.VERSION)
    return {
        MetaSectionKey.DOMAIN: domain,
        MetaSectionKey.NAME: name,
        MetaSectionKey.VERSION: version
    }


def construct_identity(meta_values):
    return '{domain}{domain_delim}{method}{version_delim}{version}'.format(
        domain=meta_values[MetaSectionKey.DOMAIN],
        domain_delim=IdentityDelimeter.DOMAIN,
        method=meta_values[MetaSectionKey.NAME],
        version_delim=IdentityDelimeter.VERSION,
        version=str(meta_values[MetaSectionKey.VERSION]),
    )


def path_for_identity(identity):
    meta_info = deconstruct_identity(identity)
    root_path = IdentityConfigs.get(IdentityConfigsKey.PATH_TO_CONTENT_ROOT)
    return '{root_path}/{domain_path}/{name}/{version}.yaml'.format(
        root_path=root_path,
        domain_path=meta_info[MetaSectionKey.DOMAIN],
        name=meta_info[MetaSectionKey.NAME],
        version=meta_info[MetaSectionKey.VERSION].replace('.', '_')
    )


def identity_for_path(*args, **kwargs):
    msg = 'Not Implemented: identity_for_path()' \
          'This is being left unimplemented as an affirmative design decision. ' \
          'Needing this function to exist should be considered a sign that you are on the Thorny Road to Sadness.' \
          'You are urged to reconsider the series of assumptions that brought you here.'
    raise NotImplementedError(msg)


def get_dotted_domain(identity):
    return deconstruct_identity(identity)[MetaSectionKey.DOMAIN].replace('/', '.')


def get_dotted_namespace(identity):
    return '.'.join([get_dotted_domain(identity), deconstruct_identity(identity)[MetaSectionKey.NAME]])
