Array = JavaClass("java.lang.reflect.Array")
Clazz = JavaClass("java.lang.Class")
Obj = JavaClass("java.lang.Object")

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

def get_private_field_value(obj, intermediary):
    cls = obj.getClass()
    
    field = cls.getDeclaredField(intermediary)
    field.setAccessible(True)
    
    return field.get(obj)

def find_method(cls, intermediary, param_types):
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
