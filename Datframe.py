import pandas as pd
df3 = pd.DataFrame(columns=['cam_left', 'cam_right', 'cam_centre', 'steering_in_value', 'steering_value', 'throttle_in_value', 'throttle_value', 'clutch_in_value', 'clutch_value', 'wheelspeed_value', 'rpmspin_value']) # modify
print(df3)
df3.to_csv("my_data_lap3.csv", index=False)