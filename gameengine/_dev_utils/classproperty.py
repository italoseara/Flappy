class classproperty(property):
    def __get__(self, _, owner_cls):
        return self.fget(owner_cls)
