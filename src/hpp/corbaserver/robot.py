#!/usr/bin/env python
# Copyright (c) 2014 CNRS
# Author: Florent Lamiraux
#
# This file is part of hpp-corbaserver.
# hpp-corbaserver is free software: you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# hpp-corbaserver is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Lesser Public License for more details.  You should have
# received a copy of the GNU Lesser General Public License along with
# hpp-corbaserver.  If not, see
# <http://www.gnu.org/licenses/>.

from hpp.corbaserver.client import Client

##
#  Helper class to load a robot model in hpp::core::ProblemSolver instance.
#
#  This class is also used to initialize a client to rviz in order to
#  display configurations of a robot.
class Robot (object):
    def __init__ (self, robotName, rootJointType):
        self.tf_root = "base_link"
        self.rootJointType = rootJointType
        self.client = Client ()
        self.loadModel (robotName, rootJointType)
        self.jointNames = self.client.robot.getJointNames ()
        self.rankInConfiguration = dict ()
        self.rankInVelocity = dict ()
        rankInConfiguration = rankInVelocity = 0
        for j in self.jointNames:
            self.rankInConfiguration [j] = rankInConfiguration
            rankInConfiguration += self.client.robot.getJointConfigSize (j)
            self.rankInVelocity [j] = rankInVelocity
            rankInVelocity += self.client.robot.getJointNumberDof (j)

    def loadModel (self, robotName, rootJointType):
        self.client.robot.loadRobotModel (robotName, rootJointType,
                                          self.packageName, self.urdfName,
                                          self.urdfSuffix, self.srdfSuffix)

    ## \name Degrees of freedom
    #  \{

    ## Get size of configuration
    # \return size of configuration
    def getConfigSize (self):
        return self.client.robot.getConfigSize ()

    # Get size of velocity
    # \return size of velocity
    def getNumberDof (self):
        return self.client.robot.getNumberDof ()
    ## \}

    ## \name Joints
    #\{

    ## Get joint names in the same order as in the configuration.
    def getJointNames (self):
        return self.client.robot.getJointNames ()

    ## Get joint position.
    def getJointPosition (self, jointName):
        return self.client.robot.getJointPosition (jointName)

    ## Get joint number degrees of freedom.
    def getJointNumberDof (self, jointName):
        return self.client.robot.getJointNumberDof (jointName)

    ## Get joint number config size.
    def getJointConfigSize (self, jointName):
        return self.client.robot.getJointConfigSize (jointName)

    ## set bounds for the joint
    def setJointBounds (self, jointName, inJointBound):
        return self.client.robot.setJointBounds (jointName, inJointBound)

    ## Set bounds on the translation part of the freeflyer joint.
    #
    #  Valid only if the robot has a freeflyer joint.
    def setTranslationBounds (self, xmin, xmax, ymin, ymax, zmin, zmax):
        self.client.robot.setJointBounds ("base_joint_x", [xmin, xmax])
        self.client.robot.setJointBounds ("base_joint_y", [ymin, ymax])
        if any("base_joint_z" in s for s in self.getJointNames()):
            self.client.robot.setJointBounds ("base_joint_z", [zmin, zmax])
        else:
            self.client.robot.setJointBounds ("base_joint_rz", [zmin, zmax])
    ## \}

    ## \name Configurations
    #\{

    ## Set current configuration of composite robot
    #
    #  \param q configuration of the composite robot
    def setCurrentConfig (self, q):
        self.client.robot.setCurrentConfig (q)

    ## Get current configuration of composite robot
    #
    #  \return configuration of the composite robot
    def getCurrentConfig (self):
        return self.client.robot.getCurrentConfig ()

    ## Shoot random configuration
    #  \return dofArray Array of degrees of freedom.
    def shootRandomConfig(self):
        return self.client.robot.shootRandomConfig ()

    ## \}

    ## \name Collision checking and distance computation
    # \{

    ## Test collision with obstacles and auto-collision.
    #
    # Check whether current configuration of robot is valid by calling
    # CkwsDevice::collisionTest ().
    # \return whether configuration is valid
    def collisionTest (self):
        return self.client.robot.collisionTest ()

    ## Compute distances between bodies and obstacles
    #
    # \return list of distances,
    # \return names of the objects belonging to a body
    # \return names of the objects tested with inner objects,
    # \return  closest points on the body,
    # \return  closest points on the obstacles
    # \note outer objects for a body can also be inner objects of another
    # body.
    def distancesToCollision (self):
        return self.client.robot.distancesToCollision ()
    ## \}
    ## \name Mass and inertia
    # \{

    ## Get mass of robot
    def getMass (self):
        return self.client.robot.getMass ()

    ## Get position of center of mass
    def getCenterOfMass (self):
        return self.client.robot.getCenterOfMass ()
    ## Get Jacobian of the center of mass
    def getJacobianCenterOfMass (self):
        return self.client.robot.getJacobianCenterOfMass ()
    ##\}

## Humanoid robot
#
#  Method loadModel builds a humanoid robot.
class HumanoidRobot (Robot):

    def __init__ (self, robotName, rootJointType):
        Robot.__init__ (self, robotName, rootJointType)
    def loadModel (self, robotName, rootJointType):
        self.client.robot.loadHumanoidModel (robotName, rootJointType,
                                          self.packageName, self.urdfName,
                                          self.urdfSuffix, self.srdfSuffix)
