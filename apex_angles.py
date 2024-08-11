import math

def reward_function(params):
    
    print("Params - ", params)

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    is_left_of_center = params['is_left_of_center']
    
    car_axle_length = 0.165
    
    reward = 1e-3
    lowest_reward = 1e-3
    speed_reward = 3
    track_reward = 2.0

    # reward for being on track
    track_width = track_width + (car_axle_length*0.5)
    marker_1 = 0.5 * track_width
    
    # Give higher reward if the car is within the track
    if distance_from_center <= marker_1:
        reward += track_reward
    else:
        return float(lowest_reward) # car is out of track
    
    steering_angle = params['steering_angle']
    speed = params['speed']
    

    # rewarding based on speed
    reward += (speed*speed_reward) * 0.25
    
    
    # reward model if it is on straight line with higher speed
    route_angle = check_waypoints_angle(params, 4) # checks next 4 waypoints angle

    # if path is straight
    if route_angle < 1.5 and speed > 3.5:
        # reduce reward if model is left side of track
        if is_left_of_center:
            reward *= 0.5
        else:
            if distance_from_center <= marker_1 and distance_from_center > (marker_1*0.3):
                # add reward for going fast in straight line
                reward = reward + (speed * 0.5)
                reward *= (1/(abs(steering_angle) + 0.65))  # 0 degree angle being highest, i.e 1.53 points multiplier
            else:
                # making car take turn to right, 
                # but limiting it to 5 degree steering angle
                reward *= (((abs(steering_angle) + 1) % 6)*0.5)
    
    # if there's a turning ahead
    # reduce reward if it goes faster than 3 ms
    elif route_angle >= 1.5:
        if speed > 3:        
            reward *= 0.5
        else:
            # reward if car turns during curves
            reward *= ((abs(steering_angle) + 1.1) % 10)
    
    # discourage angles more than 15 degree
    if steering_angle < -15 or steering_angle > 15 :
        reward *= 0.7

    # reward *= check_heading_angles(params) # reward based on where the model is heading


    return float(reward)



    
def check_waypoints_angle(params, total_waypoints):
    waypoints = params['waypoints']
    waypoints_index = params['closest_waypoints'][0]

    if waypoints_index + total_waypoints + 1 > len(waypoints):
        return 0

    # waypoint is stored as tuple of (x,y)
    w1 = waypoints[waypoints_index] 
    w2 = waypoints[waypoints_index + total_waypoints]
    return get_angle_diff(w1[0], w1[1], w2[0], w2[1])
    

def get_angle_diff(x1,y1,x2,y2):
    # Calculate the direction in radius, arctan2(dy, dx), 
    # the result is (-pi, pi) in radians between target and current vehicle position
    route_direction = math.atan2(y2 - y1, x2 - x1) 
    # Convert to degree
    angle_diff = math.degrees(route_direction)
    print("get_angle_diff ", angle_diff)

    # normalize angles wrt the quadrant axis

    angle_diff = angle_diff % 90
    if angle_diff > 45:
        return 90 - angle_diff 
    else:
        return angle_diff 


def check_heading_angles(params):
    heading_direction = params['heading']
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
    direction_diff = route_direction - heading_direction

    #Check that the direction_diff is in valid range
    #Then compute the heading reward

    print("route_direction ", route_direction)
    print("heading_direction ", heading_direction)
    print("direction_diff ", direction_diff)

    if abs(direction_diff) <= 20:
        reward = math.cos( abs(direction_diff ) * ( math.pi / 180 ) ) ** 2
    else:
        reward = math.cos( abs(direction_diff ) * ( math.pi / 180 ) ) ** 10
    
    return reward * 0.5
