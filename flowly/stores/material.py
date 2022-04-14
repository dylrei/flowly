class Material(object):
    def __init__(self, identity):
        self._identity = identity
        self._value = None  # tbd: the actual object

    @property
    def identity(self):
        return self._identity

    @property
    def value(self):
        return self._value


class Asset(Material):
    # the same, but less writeable
    pass



class MaterialStore(object):
    @classmethod
    def load_one_material(cls, identity):
        if isinstance(identity, list):
            raise RuntimeError(f'Attempt to use !Material to load array of identities: {identity}')
        return Material(identity)

    @classmethod
    def load_one_asset(cls, identity):
        if isinstance(identity, list):
            raise RuntimeError(f'Attempt to use !Asset to load array of identities: {identity}')
        return Asset(identity)

    @classmethod
    def load_many_materials(cls, identities):
        if isinstance(identities, str):
            raise RuntimeError(f'Attempt to use !Materials to load single identity: {identities}')
        return [Material(identity) for identity in identities]

    @classmethod
    def load_many_assets(cls, identities):
        if isinstance(identities, str):
            raise RuntimeError(f'Attempt to use !Assets to load single identity: {identities}')
        return [Asset(identity) for identity in identities]
