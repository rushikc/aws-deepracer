def reward_function(params):
    
    print("Params - ", params)

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    
    car_axle_length = 0.165
    
    reward = 1e-3
    lowest_reward = 1e-3
    highest_reward = 2.0

    # Calculate 3 markers that are at varying distances away from the center line
    track_width = track_width + (car_axle_length*0.5)
    marker_1 = 0.5 * track_width
    
    # Give higher reward if the car is within the track
    if distance_from_center <= marker_1:
        reward += highest_reward
    else:
        return float(reward) # car is out of track
    
    steering_angle = params['steering_angle']
    speed = params['speed']
    
    if -5 < steering_angle < 5 :
        if speed == 4:
            reward += highest_reward
        elif speed > 3.8:
            reward += (highest_reward - 0.1)
        elif speed > 3.6:
            reward += (highest_reward - 0.2)
        elif speed > 3.4:
            reward += (highest_reward - 0.3)
        elif speed > 3.2:
            reward += (highest_reward - 0.4)
        elif speed > 3:
            reward += (highest_reward - 0.5)
        elif speed > 2.8:
            reward += (highest_reward - 0.6)
    
    
    return float(reward)
