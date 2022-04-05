from .truth import SourceOfTruth
from ..constants.runtime import IdentityConfigsKey


class IdentityConfigs(SourceOfTruth):
    managed_names = {
        IdentityConfigsKey.CONTENT_ROOT: None
    }