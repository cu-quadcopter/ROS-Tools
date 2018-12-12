import rospy

'''
Adapted from `roshelper` python package
https://github.com/wallarelvo/roshelper
'''

class RosNode:

    def __init__(self, node_name, **kwargs):
        self.__node_name__ = node_name
        self.__kwargs__ = kwargs
        self.__node__ = rospy.init_node(self.__node_name__, **self.__kwargs__)

    def start(self):
        pass

    # Public Decorator To Create new Publishers
    def publisher(self, *args, **kwargs):

        # Process the function that was passed in
        # Create the publisher
        def __decorator(func):
            # args -> nameless arguments
            #     Using `args` prevents these arguments from appearing in kwargs
            topic_name, data_type = args
            # Make sure 'queue_size is in the kwargs'
            if not "queue_size" in kwargs:
                kwargs["queue_size"] = 1

            # Make the publisher
            pub = rospy.Publisher(topic_name, data_type, **kwargs)

            # Calls the decorated function
            # Passes result to the publisher
            def __inner():
                # Call the function
                msg = func()
                # Publish the result
                pub.publish(msg)

            return __inner

        return __decorator

    def subscriber(self, *args, **kwargs):
        # Process the function that was passed in
        # Creates the subscriber
        def __decorator(func):
            topic_name, data_type = args

            sub = rospy.Subscriber(topic_name, data_type, func, **kwargs)

        return __decorator

    def service(self, *args, **kwargs):
        (topic_name, data_type) = args

        def __decorator(func):
            serv = rospy.Service(topic_name, data_type, func, **kwargs)

        return __decorator
