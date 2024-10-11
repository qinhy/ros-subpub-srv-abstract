# ROS2 components : pub/sub, service

# class == Namespace Path
#   variable == Final Endpoint Namespace Path
#   function starts with "_srv_" == Service
#   function starts with "_act_" == Action

# streaming direction => input or output
#    output : Pub a topic
#    output == variable == Pub a topic

#    input  : The instance try to Sub a topic, passive  (try Sub)
#    input == try Sub == {_}variable ({__}variable is private)

import random
import string

class RosMessageBase:
    def __init__(self):
        self.__empty = True

    def __str__(self):
        # Provide a readable string representation of the object for end-users
        return '\n'.join(f"{attribute}: {value}" for attribute, value in self.__dict__.items() if not self._is_private(attribute))

    def __repr__(self):
        # Provide a more detailed string representation, useful for debugging
        class_name = self.__class__.__name__
        attributes = ', '.join(f"{attribute}={value!r}" for attribute, value in self.__dict__.items() if not self._is_private(attribute))
        return f"{class_name}({attributes})"
    
    def empty(self):
        return self.__empty

    def to_ros_bridge_format(self):
        public_data = {}
        for key, value in self.__dict__.items():
            if not key.startswith('__'):
                public_data[key] = value
        return public_data

    def from_ros_bridge_format(self, data):
        instance = self.__class__()
        instance.__dict__.update(data)
        instance.__empty = False
        self.__dict__.update(instance.__dict__)
        return self

    def get_topic_type(self):
        return self.__class__.__name__.replace('__', '/')

    def _is_private(self, param_name):
        return '__' in param_name or '/__' in param_name

    def random_set_members(self):
        def dfs_random_set(obj):
            for key, value in obj.__dict__.items():
                if not self._is_private(key) and isinstance(value, dict):
                    # Recursively set values for nested dictionaries
                    dfs_random_set(type('Temp', (object,), value)())
                elif isinstance(value, int) or isinstance(value, float):
                    obj.__dict__[key] = random.uniform(0, 10)  # Set random number, adjust range as needed
                elif isinstance(value, str):
                    obj.__dict__[key] = ''.join(random.choices(string.ascii_lowercase, k=6))  # Random 6-character string
                elif isinstance(value, bool):
                    obj.__dict__[key] = random.choice([True, False])  # Random boolean
        dfs_random_set(self)


class std_msgs__msg__Int8MultiArray(RosMessageBase):
    def __init__(self):
        super().__init__()
        self.layout = {'dim': [], 'data_offset': 0}
        self.data = []

class std_msgs__msg__Float32MultiArray(RosMessageBase):
    def __init__(self):
        super().__init__()
        self.layout = {
            'dim': [],  # array of dimensions, each with label, size, and stride
            'data_offset': 0  # offset for the data in the array
        }
        self.data = []  # array of float32 values

class std_msgs__msg__StringMessage(RosMessageBase):
    def __init__(self, data=''):
        super().__init__()
        self.data = data

# Assigning classes to std_msgs namespace
class std_msgs:
    class msg:
        Int8MultiArray = std_msgs__msg__Int8MultiArray
        Float32MultiArray = std_msgs__msg__Float32MultiArray
        StringMessage = std_msgs__msg__StringMessage

print(std_msgs.msg.Int8MultiArray())
print(std_msgs.msg.Int8MultiArray().get_topic_type())

print(std_msgs.msg.Float32MultiArray())
print(std_msgs.msg.Float32MultiArray().get_topic_type())

print(std_msgs.msg.StringMessage())
print(std_msgs.msg.StringMessage().get_topic_type())
