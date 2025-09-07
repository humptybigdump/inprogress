from opcua import Server, ua
import time
import random
from datetime import datetime, timezone


# Create and configure server
server = Server()
endpoint_url = "opc.tcp://127.0.0.1:4841"
server.set_endpoint(endpoint_url)
server.set_server_name("Workstation_Housing")

# Register namespace
uri = "http://example.org/workstation_housing/"
idx = server.register_namespace(uri)

# define root node

workstation_housing = server.nodes.objects.add_object(idx, "WorkstationHousing")


# ============================================================
# Type definitions
# ============================================================

#.....................................................................
# SENSOR
sensor_type = server.nodes.base_object_type.add_object_type(idx, "SensorType")
sensor_type.add_variable(idx, "Manufacturer", "", ua.VariantType.String).set_modelling_rule(True)
sensor_type.add_variable(idx, "SerialNumber", 0, ua.VariantType.Int64).set_modelling_rule(True)


# Temperature Sensor
temp_sensor_type = sensor_type.add_object_type(idx,"TemperatureSensorType")
measurement_temperature = temp_sensor_type.add_variable(idx,"Measurement","SensorValue")
measurement_temperature.set_modelling_rule(True)
measurement_temperature.add_variable(idx, "Value", 0.0, ua.VariantType.Double).set_modelling_rule(True)
measurement_temperature.add_property(idx,"Unit","°C",ua.VariantType.String).set_modelling_rule(True)




# Pressure Sensor
pressure_sensor_type = sensor_type.add_object_type(idx,"PressureSensorType")
measurement_pressure = pressure_sensor_type.add_variable(idx,"Measurement","")
measurement_pressure.set_modelling_rule(True)
measurement_pressure.add_variable(idx, "Value", 0.0, ua.VariantType.Double).set_modelling_rule(True)
measurement_pressure.add_property(idx,"Unit","bar",ua.VariantType.String).set_modelling_rule(True)

#....................................................................



# ============================================================
# Instances
# ============================================================



# Cooling Temperature Sensor Instance
cooling_temp_sensor = server.nodes.objects.add_object(idx,"CoolingTemperatureSensor",temp_sensor_type)
workstation_housing.add_reference(cooling_temp_sensor.nodeid,ua.ObjectIds.HasComponent)

cooling_temp_sensor.get_child("{}:Manufacturer".format(idx)).set_value("ABCCompany")
cooling_temp_sensor.get_child("{}:SerialNumber".format(idx)).set_value(48852986)
cool_measurement = cooling_temp_sensor.get_child("{}:Measurement".format(idx))
cool_measurement.get_child("{}:Value".format(idx)).set_value(5.0)





# Pressure Sensor
pressure_sensor = server.nodes.objects.add_object(idx,"PressureSensor",pressure_sensor_type)
workstation_housing.add_reference(pressure_sensor.nodeid,ua.ObjectIds.HasComponent)

pressure_sensor.get_child("{}:Manufacturer".format(idx)).set_value("MaxPowerCompany")
pressure_sensor.get_child("{}:SerialNumber".format(idx)).set_value(156846132)
pressure_measurement = pressure_sensor.get_child("{}:Measurement".format(idx))
pressure_measurement.get_child("{}:Value".format(idx)).set_value(500)

try:
    print("Server starting...")
    server.start()
    print("Server running. Press Ctrl+C to stop.")
    
    while True:
        cool_measurement.get_child("{}:Value".format(idx)).set_value(random.uniform(0.0, 25.0))
        pressure_measurement.get_child("{}:Value".format(idx)).set_value(random.uniform(500, 2000))

        # simulate or sleep
        time.sleep(1)

except KeyboardInterrupt:
    print("Interrupt received. Stopping server...")
    server.stop()
    print("Server stopped.")



