"""
    Author: JulianIsLost
    Desc: Library for accessing private fields, methods and constructors
"""
Array = JavaClass("java.lang.reflect.Array")
Clazz = JavaClass("java.lang.Class")
Obj = JavaClass("java.lang.Object")

# Pass the object to call the method on, along with the intermediary mapping of the method and its parameters
def call_private_method(obj, intermediary, *args):
    cls = obj.getClass()
    
    param_types = Array.newInstance(type(Clazz), len(args))
    params = Array.newInstance(type(Obj), len(args))
    
    for i, arg in enumerate(args):
        Array.set(param_types, i, arg.getClass())
        Array.set(params, i, arg)
        
    method = find_method(cls, intermediary, param_types)
    if method is None:
        return 
    
    method.setAccessible(True)
    return method.invoke(obj, params)

# Pass the object to get the field on, along with the intermediary mapping of the field
def get_private_field_value(obj, intermediary):
    cls = obj.getClass()
    
    field = cls.getDeclaredField(intermediary)
    field.setAccessible(True)
    
    return field.get(obj)

def set_private_field_value(obj, name, value):
    try:
        field = obj.getClass().getDeclaredField(name)
    except:
        return
    field.setAccessible(True)
    field.set(obj, value)
    print("Updated",field,"to",field.get(obj))

# Pass the class which has the constructor along with its parameters
def call_private_constructor(cls, *args)
    param_types = Array.newInstance(type(Clazz), len(args))
    params = Array.newInstance(type(Obj), len(args))
    
    for i, arg in enumerate(args):
        Array.set(param_types, i, arg.getClass())
        Array.set(params, i, arg)
    
    constructor = cls.getDeclaredConstructor(param_types)
    constructor.setAccessible(True)
    
    return constructor.newInstance(params)

def _find_method(cls, intermediary, param_types):
    while cls is not None:
        try:
            method = cls.getDeclaredMethod(intermediary, param_types)
            return method
        except:
            pass
        
        for interface in cls.getInterfaces():
            try:
                method = interface.getDeclaredMethod(intermediary, param_types)
                return method
            except:
                pass
            
        cls = cls.getSuperclass()
    
    return None
