#!/usr/bin/env python3
import rospy
import tf
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
import ik_moveit


def get_transform(object, base):
    listener = tf.TransformListener()
    listener.waitForTransform(object, base, rospy.Time(), rospy.Duration(4.0))
    while not rospy.is_shutdown():
        try:
            (trans, rot) = listener.lookupTransform(object, base, rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        return (trans, rot)


def get_model_state_client(model_name, relative_entity_name):
    rospy.wait_for_service('/gazebo/get_model_state')
    try:
        get_model_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        response = get_model_state(model_name, relative_entity_name)
        return response
    except rospy.ServiceException as e:
        print("Service call failed: %s", e)


def set_model_state_client(name, position, orientation):
    state_msg = ModelState()
    state_msg.model_name = name
    state_msg.pose.position = position
    state_msg.pose.orientation = orientation
    rospy.wait_for_service('/gazebo/set_model_state')
    try:
        set_model_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        response = set_model_state(state_msg)
        return response
    except rospy.ServiceException as e:
        print("Service call failed: %s", e)


def get_position(data):
    return data.pose.position


def get_orientation(data):
    return data.pose.orientation


def gazebo_manager(model_name, order):
    rospy.init_node('gazebo_manager')

    if order == 'transport':
        result = get_model_state_client(model_name, 'world')
        conveyor_belt_bound_start = 1.8
        conveyor_belt_bound_end = 0.3
        position = get_position(result)
        orientation = get_orientation(result)
        if position.x > conveyor_belt_bound_start:
            position.x = 1.6
            position.y = 0.4
            position.z = 0.0
            set_model_state_client(model_name, position, orientation)
        while position.x > conveyor_belt_bound_end:
            position.x -= 0.001
            set_model_state_client(model_name, position, orientation)
    elif order == 'robot_to_box':
        result = get_model_state_client(model_name,'world')
        position = [result.pose.position.x,result.pose.position.y,result.pose.position.z]
        ik_moveit.main((position,[0.707, 0.707, 0.0, 0.0]),False)
    elif order == 'robot_handled':
        ik_moveit.main(([0.256, 0.294, 0.365], [0.707, 0.707, 0.0, 0.0]),True)
        ik_moveit.main(([0.256,0.0,0.28], [0.707, 0.707, 0.0, 0.0]),True)
        ik_moveit.main(([0.256,-0.3,0.15], [0.707, 0.707, 0.0, 0.0]),True)
        result = get_model_state_client('object', 'world')
        position = get_position(result)
        orientation = get_orientation(result)
        while position.z > 0.19:
            position.z -= 0.001
            set_model_state_client('object', position, orientation)
        ik_moveit.main(([0.256,-0.25,0.25], [0.707, 0.707, 0.0, 0.0]), False)
        ik_moveit.main(([0.256, 0.0, 0.28], [0.707, 0.707, 0.0, 0.0]), False)
        ik_moveit.main(([0.256, 0.294, 0.365], [0.707, 0.707, 0.0, 0.0]), False)


if __name__ == '__main__':
    try:
        gazebo_manager('object', 'transport')
        gazebo_manager('object', 'robot_to_box')
        gazebo_manager('robot', 'robot_handled')
    except rospy.ROSInterruptException:
        pass