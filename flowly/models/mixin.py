from flowly.constants.identity import IdentityDelimeter


class MaterialMixin(object):
    barcode_prefix = None
    barcode_field_name = None

    @property
    def identity(self):
        barcode = getattr(self, self.barcode_field_name)
        return f'{self.namespace.unique_name}{IdentityDelimeter.NAMESPACE}{barcode}'