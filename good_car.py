def reward_function(params):
    
    print("Params - ", params)

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    
    car_axle_length = 0.165
    
    reward = 1e-3
    lowest_reward = 1e-3
    speed_reward = 2.5
    track_reward = 2.0

    # reward for being on track
    track_width = track_width + (car_axle_length*0.5)
    marker_1 = 0.5 * track_width
    
    # Give higher reward if the car is within the track
    if distance_from_center <= marker_1:
        reward += track_reward
    else:
        return float(reward) # car is out of track
    
    steering_angle = params['steering_angle']
    speed = params['speed']
    
    # rewarding based on speed
    reward += (speed*speed_reward) * 0.25
    
    # discourage angles more than 15 degree
    if steering_angle < -15 or steering_angle > 15 :
        reward *= 0.7
    
    return float(reward)
