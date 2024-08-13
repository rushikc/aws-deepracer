import math

# global class to store previous state
class PARAMS:
    prev_speed = None
    prev_steering_angle = None
    prev_steps = None
    prev_angle = None


def reward_function(params):
    
    print("Params - ", params)

    # Read input parameters
    track_width = params['track_width']
    steps = params['steps']
    distance_from_center = params['distance_from_center']
    current_waypoint = params['closest_waypoints'][0]


    # Reinitialize previous parameters if it is a new episode
    if PARAMS.prev_speed is None or steps < PARAMS.prev_steps:
        PARAMS.prev_speed = None
        PARAMS.prev_steering_angle = None
        PARAMS.prev_steps = None
        PARAMS.prev_angle = None

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
    route_angle = check_waypoints_angle(params, 2) # checks next 2 waypoints angle

    if PARAMS.prev_angle != None:
        route_angle_diff = route_angle - PARAMS.prev_angle
    else:
        route_angle_diff = 0

    # first track segment before start of acute turns or curves
    track1_start = -1
    track1_end = 46

    # last track segment after end of acute turns or curves
    track2_start = 98
    track2_end = 156

    # logic to hangle first & last segment track
    if track1_start < current_waypoint < track1_end or track2_start < current_waypoint < track2_end:

        # trying to go right side
        if steering_angle < 0:
            reward = lowest_reward
        else:
            # if path is straight
            if speed < 1:
                reward = lowest_reward
            elif route_angle < 1.5 :
                # add reward for going fast in straight line
                reward *= (speed * 0.5)

                if PARAMS.prev_speed != None:
                    speed_diff = speed - PARAMS.prev_speed
                    if speed_diff <= 0:
                        reward = lowest_reward
                    else:
                        reward *= ((speed_diff+1)*1.5)

            # if there's a turning ahead
            # add reward to make model stick to left steering angle ( +ve )
            elif route_angle >= 1.5:

                reward *= (speed * 0.5)
                if speed > 3.5:        
                    reward = lowest_reward
                elif route_angle_diff > 1.5:
                    if PARAMS.prev_speed != None:
                        speed_diff = speed - PARAMS.prev_speed
                        if speed_diff < 0:
                            reward *= ((abs(speed_diff)+1)*1.5)
                        else:
                            reward = lowest_reward

                if route_angle_diff < -1.5:
                    if PARAMS.prev_speed != None:
                        speed_diff = speed - PARAMS.prev_speed
                        if speed_diff <= 0:
                            reward = lowest_reward
                        else:
                            reward *= ((speed_diff+1)*1.5)            
    else:
        if speed > 3:        
            reward = lowest_reward
        elif speed < 1:
            reward = lowest_reward
        else:
            # if path is straight
            if route_angle < 1.5:

                reward *= (speed * 0.5)

                if PARAMS.prev_speed != None:
                        speed_diff = speed - PARAMS.prev_speed
                        if speed_diff <= 0:
                            reward = lowest_reward
                        else:
                            reward *= 1.7

            # if there's a turning ahead
            # reduce reward if it goes faster than 3 ms
            elif route_angle >= 1.5:
                # reward if car turns during curves
                reward *= (speed * 0.5)
                
                if route_angle_diff > 1.5:
                    if PARAMS.prev_speed != None:
                        speed_diff = speed - PARAMS.prev_speed
                        if speed_diff < 0:
                            reward *= ((abs(speed_diff)+1)*1.5)
                        else:
                            reward = lowest_reward

                if route_angle_diff < -1.5:
                    if PARAMS.prev_speed != None:
                        speed_diff = speed - PARAMS.prev_speed
                        if speed_diff <= 0:
                            reward = lowest_reward
                        else:
                            reward *= ((speed_diff+1)*1.5)
    
    # discourage angles more than 10 degree
    if steering_angle < -12 or steering_angle > 12 :
        reward = lowest_reward    
    
    # update the class variables
    PARAMS.prev_speed = speed
    PARAMS.prev_steering_angle = steering_angle
    PARAMS.prev_angle = route_angle
    PARAMS.prev_steps = steps


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

