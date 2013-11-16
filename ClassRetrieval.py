#This is so that we can import a module to be used within the ChangeState() func.
import importlib

def getClass(sClassName):
    """This takes in a string and will retrieve a class with the same name and
    return it. It assumes that the class' name is within a file with the same
    name. This class can then be used to create instances of the class."""

    module = importlib.import_module('%s'%(sClassName))

    classRef = getattr(module, sClassName)

    return classRef

