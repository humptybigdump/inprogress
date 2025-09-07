import sys
import xml.etree.ElementTree as ET

def check_temperature_sensor(xml_path, workstation_id):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Find the workstation with the specified ID
        workstation = root.find(f".//workstation[@id='{workstation_id}']")
        if workstation is None:
            print(f"No workstation found with ID {workstation_id}")
            return

        # Find all temperature sensors directly under the workstation
        temperature_sensors = workstation.findall("sensor[@type='Temperature']")
        if not temperature_sensors:
            print("No temperature sensor found")
            return

        # Check each temperature sensor for the unit
        for sensor in temperature_sensors:
            sensor_id = sensor.get('id')
            unit = sensor.get('unit')
            if unit == '°C':
                print(f"Temperature sensor {sensor_id} with the unit °C found")
            else:
                print(f"Temperature sensor {sensor_id} found but unit is not °C")

    except ET.ParseError:
        print("Error parsing the XML file")
    except FileNotFoundError:
        print(f"File not found: {xml_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_xml> <workstation_id>")
    else:
        xml_path = sys.argv[1]
        workstation_id = sys.argv[2]
        check_temperature_sensor(xml_path, workstation_id)
