# Monkey patch Django's BaseContext.__copy__ to support Python 3.14+
# Python 3.14+ restricts setting attributes on super() proxies, causing an AttributeError in Django 5.0.x

try:
    # pyrefly: ignore [missing-import]
    from django.template.context import BaseContext
    
    def patch_base_context_copy(self):
        duplicate = self.__class__.__new__(self.__class__)
        for key, value in self.__dict__.items():
            if key == 'dicts':
                duplicate.dicts = self.dicts[:]
            else:
                setattr(duplicate, key, value)
        return duplicate

    BaseContext.__copy__ = patch_base_context_copy
except ImportError:
    pass
