class SourceOfTruth(object):
    '''
    Sources of Truth are singletons that map specified keys to globally singular values
    that are immutable, once set (using public interfaces)
    Sources of Truth follow rules regarding how key/values setting may happen, specifically:
    1. Only keys that are expected may be set (i.e., they must be present in the object definition)
    2. Values are updated *only* the first time any attempt is made to set it
    3. Thereafter, any attempt to set that attribute to the same value is ignored
    4. Any attempt to set that attribute to a *new* value is treated as evidence of significant design problems
    '''
    managed_names = dict()

    def __init__(self):
        raise RuntimeError(f'Attempt to initialize SourceOfTruth subclass {self.__class__.__name__}. Please don\'t '
                           f'create multiple instances of the truth ;)')

    @classmethod
    def set(cls, key, value):
        # only names in the SOT definition are allowed
        if key not in cls.managed_names:
            raise RuntimeError(f'Attempt to set unexpected key {key} on {self.__class__.__name__}')

        current_value = cls.managed_names[key]
        if current_value is None:
            # considered declared but uninitialized, OK to initialize with new value
            cls.managed_names[key] = value
        elif current_value != value:
            # Houston, we have a problem
            raise RuntimeError(f'Attempt to set {cls.__name__} key {key} to more than one value: '
                               f'Existing value: {current_value}; Attempted Value: {value}')

    @classmethod
    def get(cls, name):
        # there should not be a default value
        return cls.managed_names[name]
