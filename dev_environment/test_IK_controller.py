import yaml
import numpy as np
import argparse

import omnigibson as og
from omnigibson.macros import gm
from omnigibson.action_primitives.starter_semantic_action_primitives import StarterSemanticActionPrimitives, StarterSemanticActionPrimitiveSet
from omnigibson.objects.primitive_object import PrimitiveObject
import omnigibson.utils.transform_utils as T
from omnigibson.objects.dataset_object import DatasetObject

import cProfile, pstats, io
import time
import os
import argparse
    

def pause(time):
    for _ in range(int(time*100)):
        og.sim.step()

def replay_controller(env, filename):
    actions = yaml.load(open(filename, "r"), Loader=yaml.FullLoader)
    for action in actions:
        env.step(action)

def execute_controller(ctrl_gen, env, filename=None):
    for action in ctrl_gen:
        env.step(action[0])

def main():
    # Load the config
    config_filename = "test_tiago.yaml"
    config = yaml.load(open(config_filename, "r"), Loader=yaml.FullLoader)

    config["scene"]["load_object_categories"] = ["floors", "ceilings", "walls", "coffee_table"]

    # Load the environment
    env = og.Environment(configs=config)
    scene = env.scene
    robot = env.robots[0]

    # Allow user to move camera more easily
    og.sim.enable_viewer_camera_teleoperation()

    table = DatasetObject(
        name="table",
        category="breakfast_table",
        model="rjgmmy",
        scale = [0.3, 0.3, 0.3]
    )
    og.sim.import_object(table)
    # table.set_position([-0.7, -2.0, 0.2])
    table.set_position([-0.7, 0.5, 0.2])
    og.sim.step()

    grasp_obj = DatasetObject(
        name="cologne",
        category="bottle_of_cologne",
        model="lyipur"
    )
    og.sim.import_object(grasp_obj)
    grasp_obj.set_position([-0.3, -0.8, 0.5])
    og.sim.step()

    controller = StarterSemanticActionPrimitives(None, scene, robot)

    def set_start_pose():
        reset_pose_tiago = np.array([
            -1.78029833e-04,  3.20231302e-05, -1.85759447e-07, -1.16488536e-07,
            4.55182843e-08,  2.36128806e-04,  1.50000000e-01,  9.40000000e-01,
            -1.10000000e+00,  0.00000000e+00, -0.90000000e+00,  1.47000000e+00,
            0.00000000e+00,  2.10000000e+00,  2.71000000e+00,  1.50000000e+00,
            1.71000000e+00,  1.30000000e+00, -1.57000000e+00, -1.40000000e+00,
            1.39000000e+00,  0.00000000e+00,  0.00000000e+00,  4.50000000e-02,
            4.50000000e-02,  4.50000000e-02,  4.50000000e-02,
        ])
        robot.set_joint_positions(reset_pose_tiago)
        og.sim.step()

    def test_navigate_to_obj():
        # Need to set start pose to reset_hand because default tuck pose for Tiago collides with itself
        # execute_controller(controller._reset_hand(), env)
        set_start_pose()
        execute_controller(controller._navigate_to_obj(table), env)

    def test_grasp_no_navigation():
        # Need to set start pose to reset_hand because default tuck pose for Tiago collides with itself
        set_start_pose()
        pose = controller._get_robot_pose_from_2d_pose([-0.433881, -0.210183, -2.96118])
        robot.set_position_orientation(*pose)
        og.sim.step()
        # replay_controller(env, "./replays/test_grasp_pose.yaml")
        execute_controller(controller._grasp(grasp_obj), env)

    def test_grasp():
        # Need to set start pose to reset_hand because default tuck pose for Tiago collides with itself
        # execute_controller(controller._reset_hand(), env)
        set_start_pose()
        # pause(2)
        execute_controller(controller._grasp(grasp_obj), env)

    def test_place():
        test_grasp()
        pause(1)
        execute_controller(controller._place_on_top(table), env)
    
    test_grasp_no_navigation()
    pause(5)



if __name__ == "__main__":
    main()



