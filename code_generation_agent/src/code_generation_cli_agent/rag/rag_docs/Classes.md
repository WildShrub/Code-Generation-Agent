The following are some best practices when creating and using classes and objects.
 
## Usually, classes should have their own file.

## Functions in a class should use type hints where possible.
    example of good practice
        class Class_Name:
            def __init__(self, name: str, x: str, y: int, z: str, is_okay: bool):
                self.name = name
                self.x = x
                self.y = y
                self.z = z
                self.is_okay = is_okay
                

            def get_name(self) -> str:
                return self.name

            def set_name(self, new_name: str) -> None:
                self.name = new_name


    example of bad practice
        class Class_Name:
            def __init__(self, name, x, y, z, is_okay):
                self.name = name
                self.x = x
                self.y = y
                self.z = z
                self.is_okay = is_okay
                

            def get_name(self):
                return self.name

            def set_name(self, new_name):
                self.name = new_name

## Functions should have a consistent naming scheme.
    example of good practice
        class Class_Name:
            def __init__(self, name: str, x: str, y: int, z: str, is_okay: bool):
                self.name = name
                self.x = x
                self.y = y
                self.z = z
                self.is_okay = is_okay
                

            def get_name(self) -> str:
                return self.name

            def set_name(self, new_name: str) -> None:
                self.name = new_name
            
            
            def get_x(self) -> str:
                return self.x

            def set_x(self, new_x: str) -> None:
                self.x = new_x


            def get_y(self) -> int:
                return self.y

            def set_y(self, new_y: int) -> None:
                self.y = new_y


            def get_z(self) -> str:
                return self.z

            def set_z(self, new_z: str) -> None:
                self.z = new_z
            

            def get_is_okay(self) -> bool:
                return self.is_okay

            def set_is_okay(self, new_is_okay) -> None:
                self.is_okay = new_is_okay


    example of bad practice
        class Class_Name:
            def __init__(self, name: str, x: str, y: int, z: str, is_okay: bool):
                self.name = name
                self.x = x
                self.y = y
                self.z = z
                self.is_okay = is_okay


            def get_name(self) -> str:
                return self.name

            def set_name(self, new_name: str) -> None:
                self.name = new_name


            def get_x(self) -> str:
                return self.x

            def set_x(self, new_x: str) -> None:
                self.x = new_x


            def getY(self) -> int:
                return self.y

            def setY(self, new_y: int) -> None:
                self.y = new_y


            def find_z(self) -> str:
                return self.z

            def change_z(self, new_z: str) -> None:
                self.z = new_z


            def get_is_Okay(self) -> bool:
                return self.is_okay

            def set_okay(self, new_is_okay) -> None:
                self.is_okay = new_is_okay

## Every variable in a class should have a get function and a set function.
    example of good practice
    
        def get_satisfaction(self) -> str:
            return self.satisfaction

        def set_satisfaction(self, new_satisfaction: str) -> None:
            self.satisfaction = new_satisfaction

## When possible, you should use the get and set functions to access variables of objects rather than calling them directly.
    example of good practice:

        old_satisfaction = customers.get_satisfaction()
        customers.set_satisfaction(new_satisfaction="high")
    
    example of bad practice:

        old_satisfaction = customers.satisfaction
        customers.satisfaction = "high"

## get and set functions should always be grouped by variable, get should always come before set, and should be in the same order as the initialization function.
    example of good practice
        class Class_Name:
            def __init__(self, name: str, x: str, y: int, z: str, is_okay: bool):
                self.name = name
                self.x = x
                self.y = y
                self.z = z
                self.is_okay = is_okay
                

            def get_name(self) -> str:
                return self.name

            def set_name(self, new_name: str) -> None:
                self.name = new_name
            
            
            def get_x(self) -> str:
                return self.x

            def set_x(self, new_x: str) -> None:
                self.x = new_x


            def get_y(self) -> int:
                return self.y

            def set_y(self, new_y: int) -> None:
                self.y = new_y


            def get_z(self) -> str:
                return self.z

            def set_z(self, new_z: str) -> None:
                self.z = new_z
            

            def get_is_okay(self) -> bool:
                return self.is_okay

            def set_is_okay(self, new_is_okay) -> None:
                self.is_okay = new_is_okay


    example of bad practice
        class Class_Name:
            def __init__(self, name: str, x: str, y: int, z: str, is_okay: bool):
                self.name = name
                self.x = x
                self.y = y
                self.z = z
                self.is_okay = is_okay
            

            def set_name(self, new_name: str) -> None:
                self.name = new_name

            def get_name(self) -> str:
                return self.name


            def get_y(self) -> int:
                return self.y

            def set_y(self, new_y: int) -> None:
                self.y = new_y


            def get_x(self) -> str:
                return self.x

            def set_x(self, new_x: str) -> None:
                self.x = new_x


            def get_z(self) -> str:
                return self.z


            def get_is_okay(self) -> bool:
                return self.is_okay


            def set_z(self, new_z: str) -> None:
                self.z = new_z


            def set_is_okay(self, new_is_okay) -> None:
                self.is_okay = new_is_okay


## Class constants should be entirely capital letters, and should be should be set directly after the init function.
    example of good practice
        class Class_Name:
            def __init__(self, name: str, x: str, y: int, z: str, is_okay: bool):
                self.name = name
                self.x = x
                self.y = y
                self.z = z
                self.is_okay = is_okay
                
            AVAGADROS_NUMBER = 602214076000000000000000

            def get_name(self) -> str:
                return self.name

            def set_name(self, new_name: str) -> None:
                self.name = new_name
            
            
            def get_x(self) -> str:
                return self.x

            def set_x(self, new_x: str) -> None:
                self.x = new_x


            def get_y(self) -> int:
                return self.y

            def set_y(self, new_y: int) -> None:
                self.y = new_y


            def get_z(self) -> str:
                return self.z

            def set_z(self, new_z: str) -> None:
                self.z = new_z
            

            def get_is_okay(self) -> bool:
                return self.is_okay

            def set_is_okay(self, new_is_okay) -> None:
                self.is_okay = new_is_okay


    example of bad practice
        class Class_Name:
            def __init__(self, name: str, x: str, y: int, z: str, is_okay: bool):
                self.name = name
                self.x = x
                self.y = y
                self.z = z
                self.is_okay = is_okay
                

            def get_name(self) -> str:
                return self.name

            def set_name(self, new_name: str) -> None:
                self.name = new_name
            
            
            def get_x(self) -> str:
                return self.x

            def set_x(self, new_x: str) -> None:
                self.x = new_x


            def get_y(self) -> int:
                return self.y

            def set_y(self, new_y: int) -> None:
                self.y = new_y


            def get_z(self) -> str:
                return self.z

            def set_z(self, new_z: str) -> None:
                self.z = new_z
            

            def get_is_okay(self) -> bool:
                return self.is_okay

            def set_is_okay(self, new_is_okay) -> None:
                self.is_okay = new_is_okay

            AVAGADROS_NUMBER = 602214076000000000000000