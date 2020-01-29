import pandas as pd
import numpy as np

import os
def main() -> None:
    from beamngpy import BeamNGpy, Scenario, Vehicle, beamngcommon
    from beamngpy.sensors import Damage, Camera, Electrics
    from time import sleep
    bng = BeamNGpy("localhost", 64523)
    ego_vehicle = Vehicle('ego_vehicle', model='etk800', licence='EGO', color='Red')

    scenario = Scenario("west_coast_usa", "DamageSensorTest", authors="Stefan Huber", description="Test usage and check output of the damage sensor")


    direction = (0, 1, 0)
    fov = 120
    resolution = (320, 160)
    y,z = (1.7, 1.0)
    cam_center = Camera((-0.3, y, z), direction, fov, resolution, colour=True, depth=True, annotation=True)
    cam_left = Camera((-1.3, y, z), direction, fov, resolution, colour=True, depth=True, annotation=True)
    cam_right = Camera((0.4, y, z), direction, fov, resolution, colour=True, depth=True, annotation=True)
    #cameras_array = [camera_center, camera_left, camera_right]

    ego_vehicle.attach_sensor('cam_center', cam_center)
    ego_vehicle.attach_sensor('cam_left',cam_left)
    ego_vehicle.attach_sensor('cam_right', cam_right)
    ego_vehicle.attach_sensor("electrics", Electrics())
    #electrics_data = Electrics.encode_vehicle_request(Electrics)
    #print(electrics_data)
    #scenario.add_vehicle(ego_vehicle,pos=(-717.121, 101, 118.675), rot=(0, 0, 45))
    scenario.add_vehicle(ego_vehicle, pos=(-725.7100219726563,554.3270263671875,121.0999984741211), rot=(0,0,45))
    scenario.make(bng)
    bng.open(launch = True)

    def save_image(data, ind, cam_name):
        img = data[cam_name]['colour'].convert('RGB')

        file_name = str(ind) + "_" + cam_name + ".jpg"
        filepath = os.path.join('C:/Users/HP/Documents/Data_Log/10_lap_log',
                                file_name)
        img.save(filepath)
        return file_name

    def save(data, ind):
        cam_left_file_name = save_image(data, ind, 'cam_left')
        cam_right_file_name = save_image(data, ind, 'cam_right')
        cam_center_file_name = save_image(data, ind, 'cam_center')
        steering_in_value = data['electrics']['values']['steering_input']
        steering_value = data['electrics']['values']['steering']
        throttle_in_value = data['electrics']['values']['throttle_input']
        throttle_value = data['electrics']['values']['throttle']
        clutch_value = data['electrics']['values']['clutch']
        clutch_in_value = data['electrics']['values']['clutch_input']
        wheel_speed_value = data['electrics']['values']['wheelspeed']
        rpmspin_value = data['electrics']['values']['rpmspin']
        #add here


        print(cam_left_file_name, cam_right_file_name, cam_center_file_name, steering_in_value, steering_value, throttle_in_value,throttle_value, clutch_in_value,clutch_value,rpmspin_value,wheel_speed_value)
        print()

        temp_df = temp_dataframe()
        temp_df.loc[0] = [cam_left_file_name, cam_right_file_name, cam_center_file_name, steering_in_value, steering_value, throttle_in_value, throttle_value, clutch_in_value, clutch_value, wheel_speed_value, rpmspin_value] # modify

        #append with existing and save
        df_orig = pd.read_csv('my_data_lap3.csv')
        df_orig = pd.concat([df_orig, temp_df])
        df_orig.to_csv('my_data_lap3.esc', index=False)
        del [[df_orig, temp_df]]


    def temp_dataframe():
        df1 = pd.DataFrame(columns=['cam_left', 'cam_right', 'cam_centre', 'steering_in_value', 'steering_value', 'throttle_in_value', 'throttle_value', 'clutch_in_value', 'clutch_value', 'wheelspeed_value', 'rpmspin_value']) # modify
        return df1

    try:

        bng.load_scenario(scenario)
        bng.set_steps_per_second(60)
        bng.set_deterministic()
        bng.start_scenario()
        bng.hide_hud()
        ego_vehicle.ai_drive_in_lane(lane=True)
        ego_vehicle.ai_set_mode('span')
        ego_vehicle.ai_set_speed(10)

        ind = 0
        while True:
            sensor_data = bng.poll_sensors(ego_vehicle)
            save(sensor_data, ind)
            ind += 1
    finally:
        bng.close()


if __name__ == "__main__":
    main()