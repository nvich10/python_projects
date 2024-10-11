"""
Author: Noah Vich
    
"""


#Begin Code
from abc import ABC, abstractmethod
from argparse import ArgumentParser
parser = ArgumentParser()
import sys
import random
import string

class Battery :
    """The battery class allows users to create battery objects with attributes: battery_id, battery_type, battery_level.
    """
    battery_rules = {"nuclear":10000,"lithium_ion":200,"lithium_polymer":175,"nickel_hydride":150,"lead_acid":100}
    
    def __init__ (self, battery_id, battery_type) :
        """Initializes the battery object.

        Args:
            battery_id (str): A unique identifier for the battery
            battery_type (str): Must be an accepted type of battery, ex: lithium_ion
        
        Not in args:
            battery_level (float): Initialized to 0.0
        """
        self._battery_id = battery_id
        self._battery_type = battery_type

        #verify battery type
        if battery_type not in ["lithium_ion", "lithium_polymer", "nickel_hydride", "lead_acid", "nuclear"] :
            self._battery_type = None
            self._battery_level = None
        else:
            self._battery_type = battery_type
            self._battery_level = 0.0 #BE AWARE OF MAX VALUES BY battery_type
    
    def charge_battery (self, amount) :
        """Allows robot battery to be charged.

        Args:
            amount (float): Amount to charge battery 
        """
        self._battery_level += amount
        
        if self._battery_type == "lithium_ion" and self._battery_level > 200 :
            self._battery_level = 200
            
        if self._battery_type == "lithium_polymer" and self._battery_level > 175 :
            self._battery_level = 175
            
        if self._battery_type == "nickel_hydride" and self._battery_level > 150 :
            self._battery_level = 150
            
        if self._battery_type == "lead_acid" and self._battery_level > 100 :
            self._battery_level = 100
            
        if self._battery_type == "nuclear" and self._battery_level > 10000 :
            self._battery_level = 10000
    
    def consume_battery (self, amount) :
        """Consumes robot battery.

        Args:
            amount (float): Amount to consume battery by.
        """
        if (self._battery_level - amount) <= 0:
            self._battery_level = 0
        else:
            self._battery_level -= amount
            
            
    @property
    def battery_type (self) :
        return self._battery_type
    
    @battery_type.setter
    def battery_type (self, battery_type) :
        if battery_type not in ["lithium_ion", "lithium_polymer", "nickel_hydride", "lead_acid", "nuclear"] :
            self._battery_type = None
            self._battery_level = None
        else:
            self._battery_type = battery_type
            self._battery_level = 0.0 #BE AWARE OF MAX VALUES BY battery_type
            
    @property
    def battery_id (self) :
        return self._battery_id
    
    @battery_id.setter
    def battery_id (self, battery_id) :
        self._battery_id = battery_id
        
    @property
    def battery_level (self) :
        return self._battery_level
    
    @battery_level.setter
    def battery_level (self, battery_level) :
        self._battery_level = battery_level
     
            
    def __str__(self):
        return f"battery_id ( {self._battery_id} ) battery_type ( {self.battery_type} ) battery_level ( {self._battery_level} )"
        
        
    
class Motor :
    """The motor class allows users to create motor object with parameters: motor_id, motor_type, current_rating, speed.
    """
    motor_types = ["dc_motor","stepper_motor","servo_motor"]
    def __init__ (self, motor_id, motor_type, current_rating, speed) :
        """Initializes a motor object.

        Args:
            motor_id (str): unique identifier for the motor
            motor_type (str): type of motor
            current_rating (float): rating of motor
            speed (int): speed of the motor
            
        Not in args:
            state (int): 1 for on, 0 for off
        """
        self._motor_id = motor_id

        if speed > 0 and speed <= 8 :
            self._speed = speed
        else:
            self._speed = None   
        
        if current_rating > 0 and current_rating <= 5 :
            self._current_rating = current_rating
        else:
            self._current_rating = None
        
        if motor_type not in ['dc_motor', 'stepper_motor', 'servo_motor'] :
            self._motor_type = None
        else:
            self._motor_type = motor_type
            
        
        self._state = 1
        
    def start_motor (self) :
        """Start motor, motor = 1
        """
        self._state = 1
        
    def stop_motor (self) :
        """Stop motor, motor = 0
        """
        self._state = 0
        
    def step_consumption_cost(self):
        """Determines consumption cost of motor.

        Returns:
            int: Amount to consume for each movement.
        """
    #couldn't get match to work, using if-else-if instead
        if self._motor_type == 'dc_motor' :
            return 3
        elif self._motor_type == 'stepper_motor' :
            return 2
        elif self._motor_type == 'servo_motor' :
            return 1
        else:
            print('No motor type set!')
            return 0
        
    @property
    def motor_id (self) :
        return self._motor_id
    
    @motor_id.setter
    def motor_id (self, motor_id) :
        self._motor_id = motor_id
        
    @property
    def motor_type (self) :
        return self._motor_type
    
    @motor_type.setter
    def motor_type (self, motor_type) :
        if motor_type not in ['dc_motor', 'stepper_motor', 'servo_motor'] :
            self._motor_type = None
        else:
            self._motor_type = motor_type
        
    @property
    def current_rating (self) :
        return self._current_rating
    
    @current_rating.setter
    def current_rating (self, current_rating) :
        if current_rating > 0 and current_rating <= 5 :
            self._current_rating = current_rating
        else:
            self._current_rating = None
                    
    @property
    def speed (self) :
        return self._speed
    
    @speed.setter
    def speed (self, speed) :
        if speed > 0 and speed <= 8 :
            self._speed = speed
        else:
            self._speed = None
            
    @property
    def state (self) :
        return self._state
    
    @state.setter
    def state (self, state) :
        self._state = state
        
        
    def __str__ (self) :    
        return f"motor_id ( {self._motor_id} ) motor_type ({self._motor_type} ) current_rating ({self._current_rating} ) speed ( {self._speed} ) state ({self._state})"
    


class Item :
    """Allows users to declare an item object with parameters: item_type, color.
    """
    def __init__ (self, item_type, color) :
        """Initializes an item object.

        Args:
            item_type (str): Type of item, must be an accepted shape.
            color (any value): Color of the item.
        """
        self._color = color
        
        if item_type in ["cube", "cylinder", "cone", "sphere", "pyramid"] :
            self._item_type = item_type
        else:
            self._item_type = None
                
    @property
    def color (self) :
        return self._color
    
    @color.setter
    def color (self, color) :
        self._color = color
    
    @property
    def item_type (self) :
        return self._item_type
    
    @item_type.setter
    def item_type (self, item_type) :
        if item_type in ["cube", "cylinder", "cone", "sphere", "pyramid"] :
            self._item_type = item_type
        else:
            self._item_type = None
            
            
class Robot (ABC):
    """The robot class allows users to create robot objects with attributes: 
        robot_id, battery, motor, x_pos, y_pos, items
    """
        
    def __init__(self, robot_id, battery, motor, x_pos = 0, y_pos = 0) :
        """
        Initializes robot object with passed values as attributes.

        Args:
            robot_id (str): ID of robot object
            battery (Battery): battery object of robot
            motor (Motor): motory object of robot
            x_pos (int, optional): X position of robot. Defaults to 0.
            y_pos (int, optional): Y position of robot. Defaults to 0.
            
        Initialized but not passed as parameter:
            items (dict): dictionary of the items collected
            
        """
        self._robot_id = robot_id
        self._x_pos = x_pos
        self._y_pos = y_pos
        self._battery = battery
        self._motor = motor
        
        self._items = []
            
    #Methods
    
    def move_forward(self, amount) :
        """Allows robot to update position in the positive y direction
        """
        for move in range(0, amount) :
            if self._battery._battery_level > 0 and self._motor._state == 1:
                self._y_pos += 1
                self._battery.consume_battery(self._motor.step_consumption_cost())
                
    
    def move_backward(self, amount) :
        """Allows robot to update position in the negative y direction
        """
        for move in range(0, amount) :
            if self._battery._battery_level > 0 and self._motor._state == 1:
                self._y_pos -= 1
                self._battery.consume_battery(self._motor.step_consumption_cost())
                
    
    def move_right(self, amount) :
        """Allows robot to update position in the positive x direction
        """
        for move in range(0, amount) :
            if self._battery._battery_level > 0 and self._motor._state == 1:
                self._x_pos += 1
                self._battery.consume_battery(self._motor.step_consumption_cost())
                
    
    def move_left (self, amount) :
        """Allows robot to update position in the negative x direction
        """
        for move in range(0, amount) :
            if self._battery._battery_level > 0 and self._motor._state == 1:
                self._x_pos -= 1
                self._battery.consume_battery(self._motor.step_consumption_cost())
                
    @abstractmethod
    def collect_item (self, item) :
        """Allows robot to collect an item and store in items dictionary

        Args:
            item (Item): item robot has collected
        """
        if item in self._items :
            count = self._items[item]
            self._items[item] = count + 1
        else :
            self._items[item] = 1
            
    @abstractmethod         
    def drop_item (self, item_type, color) :
        """Allows robot to drop an item and update items dictionary

        Args:
            item_type (Item): item robot will drop
            color (str) : color of item
        """
        if item_type in self._items:
            count = self._items[item_type]
            self._items[item_type] = count - 1
            
    @abstractmethod
    def print_items (self) :
        """Prints the items the robot currently has in posession
        """
        for key, value in self._items.items() :
            print(f"{value} {key}")
                
        
    def charge_battery (self, amount) :
        """Chargest the robots battery

        Args:
            amount (float): amount battery is charged
        """
        self._battery.charge_battery(amount)
        

    def get_battery_level (self) :
        """Returns the battery level

        Returns:
            float: battery level
        """
        return self._battery._battery_level
    
    def get_position (self) :
        """Returns the robot position

        Returns:
            tuple: robot position (x,y)
        """
        return (self._x_pos, self._y_pos)
    
    def reset_position (self) :
        """Resets robot position to (0,0)
        """
        self._x_pos = 0
        self._y_pos = 0
        
        
    @property
    def robot_id (self) :
        return self._robot_id
    
    @robot_id.setter
    def robot_id (self, robot_id) :
        self._robot_id = robot_id 
        
    @property
    def x_pos (self) :
        return self._x_pos
    
    @x_pos.setter
    def x_pos (self, x_pos) :
        self._x_pos = x_pos
        
    @property
    def y_pos (self) :
        return self._y_pos
    
    @y_pos.setter
    def y_pos (self, y_pos) :
        self._y_pos = y_pos
        
    @property
    def items (self) :
        return self._items
    
    @items.setter
    def items (self, item) :
        self._items = [item]
        
    @property
    def battery (self) :
        return self._battery
    
    @property
    def motor (self) :
        return self._motor
                          
    
    #str
    def __str__ (self) :
        return f"Robot_id: {self._robot_id} \n\tbattery: {self._battery} \n\tmotor: {self._motor}" \
               f" \n\tx_pos: {self._x_pos} y_pos: {self._y_pos}"
    
    #repr
    def __repr__ (self) :
        return f"Robot_id: {self._robot_id} \n\tbattery: {self._battery} \n\tmotor: {self._motor}" \
               f" \n\tx_pos: {self._x_pos} y_pos: {self._y_pos}"
                
            
            
class ServiceRobot (Robot) :
    """Declares service robot objects.

    Args:
        Robot (Class): Robot class inherited
    """
    def __init__ (self, robot_id, battery, motor, x_pos = 0, y_pos = 0) :
        """Initializes service robot.
        """
        #inherited from Robot
        super().__init__(robot_id, battery, motor, x_pos, y_pos)
        
                        
    def collect_item (self, item) :
        """Appends items collected to list.

        Args:
            item (Class): The item object collected
        """
        self._items.append(item)
    
    def drop_item (self, color, item_type) :
        """If the object exists, it is dropped from items list.

        Args:
            color (str): color of item object
            item_type (str): type of item object
        """
        index = 0
        for item in self._items :
            if item_type in ["cube", "cylinder", "cone", "sphere", "pyramid"] :
                del self._items[index]
                break
            index += 1

            
    def print_items(self) :
        """Prints the item objects in items list.
        """
        for item in self._items :
            print(f"{item}\n")
            
    def __str__(self):
        return f"Robot_id: {self._robot_id} \n\tbattery: {self._battery} \n\tmotor:{self._motor}\n\tx_pos: {self._x_pos} y_pos: {self._y_pos}"
            


  
#parse args should recieve an argument list from the command prompt      
def parse_args(args_list) :
    """Takes a list of strings from the command prompt and passes them through as arguments.

    Args:
        args_list (list): list of strings from command prompt

    Returns:
        args: ArgumentParser
    """
    numservicerobots = parser.add_argument("numservicerobots", type = int, help = "A list of strings passed as arguments")
    args = parser.parse_args(args_list)
    if args.numservicerobots <= 0 :
        raise ValueError("numservicerobots must be greater than 0")
    return args


          
def main(numservicerobots):
    battery1 = Battery("1234abyz","lithium_ion")
    motor1 = Motor("M1A2B","servo_motor",3,4)
    servicerobot1 = ServiceRobot("123ABX", battery1, motor1,0,0)
    print(servicerobot1)
    print(repr(servicerobot1))
    item1 = Item("cylinder","blue")
    servicerobot1.collect_item(item1)
    print("----********----")
    random.seed(5)
    myrobotlist = []
    for x in range(0, numservicerobots):
    # TODO randomly choose battery and motor parameters
        batteryrulekeys = list(Battery.battery_rules.keys())
        rbatindex = random.randint(0,(len(batteryrulekeys)-1))
        print("----rbatindex----",rbatindex)
        batterytype1 = batteryrulekeys[rbatindex]
        print("----batterytype1----",batterytype1)
        randlet1 = random.choice(string.ascii_letters)
        randlet2 = random.choice(string.ascii_letters)
        randnum1 = random.randint(0,9)
        randnum2 = random.randint(0,9)
        batteryid1 = randlet1 + randlet2 + str(randnum1) + str(randnum2)
        battery1 = Battery(batteryid1,batterytype1)
        randlet1 = random.choice(string.ascii_letters)
        randlet2 = random.choice(string.ascii_letters)
        randlet3 = random.choice(string.ascii_letters)
        randnum1 = random.randint(0,9)
        randnum2 = random.randint(0,9)
        randnum3 = random.randint(0,9)
        motorid1 = randlet1 + randlet2 + str(randnum1) + str(randnum2) + randlet3 + str(randnum3)
        mtypeindex = random.randint(0,(len(Motor.motor_types)-1))
        motortype = Motor.motor_types[mtypeindex]
        motor1 = Motor(motorid1,motortype,3,4)
        randlet1 = random.choice(string.ascii_letters)
        randlet2 = random.choice(string.ascii_letters)
        randlet3 = random.choice(string.ascii_letters)
        randlet4 = random.choice(string.ascii_letters)
        randnum1 = random.randint(0,9)
        randnum2 = random.randint(0,9)
        randnum3 = random.randint(0,9)
        randnum4 = random.randint(0,9)
        robotid1 = randlet1 + randlet2 + str(randnum1) + str(randnum2) + randlet3 + str(randnum3)+ randlet4 + str(randnum4)
        service_robot = ServiceRobot(robotid1, battery1, motor1,0,0)
        myrobotlist.append(service_robot)
        print(service_robot)
    print("----LENGTH OF THE ROBOT LIST----")
    print(len(myrobotlist))
    item1 = Item("cone","blue")
    item2 = Item("cone","blue")
    item3 = Item("cube","green")
    myrobotlist[0].collect_item(item1)
    myrobotlist[0].collect_item(item2)
    myrobotlist[0].collect_item(item3)
    print(myrobotlist[0])
    print(myrobotlist[0].print_items())
    myrobotlist[0].drop_item("blue","cone")
    myrobotlist[0].drop_item("yellow","cone")
    print('\n\nHERE\n\n')
    myrobotlist[0]._motor.start_motor()
    myrobotlist[0].move_forward(5)
    # Should not have moved because we did not charge it yet
    assert myrobotlist[0].x_pos == 0.0, ("Robot moved but we did not charge it yet")
    myrobotlist[0].charge_battery(100)
    myrobotlist[0].move_forward(5)
    print('\n\n', myrobotlist[0], '\n\n')
    myrobotlist[0].move_right(4)
    myrobotlist[0].move_backward(2)
    myrobotlist[0].move_left(2)
    print(myrobotlist[0])
    myrobotlist[0].move_forward(500)
    print(myrobotlist[0])

if __name__ == "__main__":
    try:
        arguments = parse_args(sys.argv[1:])
        main(arguments.numservicerobots)
    except ValueError as e:
    #sys.exit(str(e))
        main(1) # This is a 'hack' to be able to run in VS code