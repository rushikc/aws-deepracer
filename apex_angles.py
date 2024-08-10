import math

def reward_function(params):
    
    print("Params - ", params)

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    
    car_axle_length = 0.165
    
    reward = 1e-3
    lowest_reward = 1e-3
    highest_reward = 2.0

    # reward for being on track
    track_width = track_width + (car_axle_length*0.5)
    marker_1 = 0.5 * track_width
    
    # Give higher reward if the car is within the track
    if distance_from_center <= marker_1:
        reward += highest_reward
    else:
        return float(reward) # car is out of track
    
    steering_angle = params['steering_angle']
    speed = params['speed']
    
    # rewarding based on speed
    reward += (speed*highest_reward) * 0.25
    
    # discourage angles more than 15 degree
    if steering_angle < -15 or steering_angle > 15 :
        reward *= 0.7
    else:
        reward += check_heading_angles(params) # reward based on where the model is heading

    return float(reward)


def check_heading_angles(params):
    heading = params['heading']
    waypoints = params['waypoints']
    vehicle_x = params['x']
    vehicle_y = params['y']
    next_way_point_index = params['closest_waypoints'][1]
    next_route_point_x = waypoints[next_way_point_index][0]
    next_route_point_y = waypoints[next_way_point_index][1]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians between target and current vehicle position
    route_direction = math.atan2(next_route_point_y - vehicle_y, next_route_point_x - vehicle_x) 
    # Convert to degree
    route_direction = math.degrees(route_direction)
    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = route_direction - heading
    #Check that the direction_diff is in valid range
    #Then compute the heading reward
    
    if abs(direction_diff) <= 20:
        reward = math.cos( abs(direction_diff ) * ( math.pi / 180 ) ) ** 2
    else:
        reward = math.cos( abs(direction_diff ) * ( math.pi / 180 ) ) ** 10
    
    return reward * 0.5
    

    