import sys
sys.path.insert(0, "..")
import time

from opcua import ua, Server

if __name__ == "__main__":

    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4842/freeopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    uri = "https://www.irs.kit.edu/EDrive/"
    idx = server.register_namespace(uri)

    
    # Define a custom ObjectType: PumpType
    robot_Mike_type = server.nodes.base_object_type.add_object_type(idx, "RobotType")

    # Add variables to the type
    robot_Mike_type.add_variable(idx, "Speed", 0.0).set_modelling_rule(True)
    robot_Mike_type.add_variable(idx, "Nb_Joints", 7.0).set_modelling_rule(True)
    
    # Add methods (simplified, no implementation here)
    def start_method(parent):
        print("Robot started")

    def stop_method(parent):
        print("Robot stopped")

    robot_Mike_type.add_method(idx, "Start", start_method, [], [])
    robot_Mike_type.add_method(idx, "Stop", stop_method, [], [])


    # Instantiate an object of PumpType
    objects = server.get_objects_node()
    Robot1 = objects.add_object(idx, "Sven", robot_Mike_type)
    Robot100 = objects.add_object(idx, "Jan", robot_Mike_type)

    # Set initial values
    ###pump1.get_child(["{}:Speed".format(idx)]).set_value(1500.0)
    ###pump1.get_child(["{}:Temperature".format(idx)]).set_value(75.0)


    # starting!
    server.start()
    
    
    try:
        count = 0
        while True:
            time.sleep(1)
            count += 0.1
            Robot1.get_child(["{}:Speed".format(idx)]).set_value(count)
            #myvar.set_value(4+count)
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()