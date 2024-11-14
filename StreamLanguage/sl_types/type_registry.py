class TypeRegistry:
    """
    A global registry for managing type conversions and custom SLType registrations.
    """
    _type_registry = {}
    _conversion_registry = {}
    _global_namespace = {}

    @classmethod
    def register_type(cls, meta_type, instance_type):
        """
        Register a type in the global type registry, attach the meta_type to the instance_type, and allow the
        meta_type's name to be used as a callable constructor for the instance_type.
        """
        # Register the type in the registry
        cls._type_registry[meta_type] = instance_type

        # Attach the meta type to the instance type
        instance_type.type_descriptor = meta_type

        # Add the callable to the global namespace using meta_type's name
        if hasattr(meta_type, 'name'):
            cls._global_namespace[meta_type.name] = instance_type

    @classmethod
    def register_conversion(cls, from_type, to_type, conversion_func):
        """
        Register a conversion function from one type to another.
        """
        cls._conversion_registry[(from_type, to_type)] = conversion_func

    @classmethod
    def get_instance_type(cls, meta_type):
        """
        Get the instance type corresponding to the given meta type.
        """
        return cls._type_registry.get(meta_type)

    @classmethod
    def convert(cls, from_instance, to_meta_type):
        """
        Convert one instance type to another using the registered conversion function.
        """
        conversion_func = cls._conversion_registry.get((type(from_instance), to_meta_type))
        if conversion_func:
            return conversion_func(from_instance)
        raise TypeError(f"Cannot convert {from_instance} to {to_meta_type}")

    @classmethod
    def get_constructor(cls, type_name):
        """
        Return the constructor for the given type name.
        """
        return cls._global_namespace.get(type_name)

    @classmethod
    def invoke_constructor(cls, type_name, *args):
        """
        Dynamically invoke the constructor for the given type name.
        """
        constructor = cls.get_constructor(type_name)
        if constructor:
            return constructor(*args)
        raise TypeError(f"No constructor found for type '{type_name}'")

    @classmethod
    def get_meta_type_by_name(cls, name):
        """
        Get the meta type by its name.
        """
        for meta_type in cls._type_registry.keys():
            if meta_type.name == name:
                return meta_type
        return None

    def get_meta_type_by_canonical_name(cls, name):  # I was going to use this method to get the meta type by its canonical name, but instead I used the get_meta_type_by_name method.
        """
        Get the meta type by its canonical name.
        """
        for meta_type in cls._type_registry.keys():
            if meta_type.canonical_name == name:
                return meta_type
        return None

    def get_meta_type_by_instance(cls, instance):
        """
        Get the meta type by its instance.
        """
        for meta_type in cls._type_registry.keys():
            if meta_type == instance.type_descriptor:
                return meta_type
        return None

    @classmethod
    def dump_registry(cls):
        """
        Debugging method to view current registered sl_types.
        """
        print("Registered Types:")
        for meta_type, instance_type in cls._type_registry.items():
            print(f"{meta_type.name}: {instance_type}")

        print("\nGlobal Namespace:")
        for type_name, instance_type in cls._global_namespace.items():
            print(f"{type_name}: {instance_type}")

# Global type registry instance
type_registry = TypeRegistry()
