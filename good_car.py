def reward_function(params):
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    reward = 1e-3
    
    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward += 2.0
    elif distance_from_center <= marker_2:
        reward += 0.5
    elif distance_from_center <= marker_3:
        reward += 0.1
    
    steering_angle = params['steering_angle']
    speed = params['speed']
    
    if -5 < steering_angle < 5 :
        if speed > 2.5:
            reward += 2.0
        elif speed > 2.0:
            reward += 1.0
    elif steering_angle < -15 or steering_angle > 15 :
        if speed < 1.8:
            reward += 1.0
        elif speed < 2.2:
            reward += 0.5
    
    #steps = params['steps']
    #progress = params['progress']
    #step_rewards = ( progress / steps) * 10
    #reward += step_rewards
    return float(reward)