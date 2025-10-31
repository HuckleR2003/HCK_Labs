"""import_core
Central registry for components. All modules register here using register_component.
This helps decoupling and allows startup.py to import modules and access them via COMPONENTS.
""" 
COMPONENTS = {}
def register_component(name, obj):
    COMPONENTS[name] = obj
    return obj
