# Make sure to have the server side running in CoppeliaSim: 
# in a child script of a CoppeliaSim scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

try:
    import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

import time
import math
print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
if clientID!=-1:
    # robotBase =sim.sim.simxGetObjectHandle(clientID,"P_Arm_joint2",sim.simx_opmode_oneshot_wait)
    print ('Connected to remote API server')
    ec,P_Arm_joint2 =sim.simxGetObjectHandle(clientID,"P_Arm_joint2",sim.simx_opmode_blocking)
    print(P_Arm_joint2)
    print (ec)
    ec,P_Arm =sim.simxGetObjectHandle(clientID,"P_Arm",sim.simx_opmode_blocking)
    print(P_Arm)
    print (ec)
    ec,flr = sim.simxGetObjectHandle(clientID,"Floor",sim.simx_opmode_blocking)
    print(flr)
    print (ec)
    ec,P_Arm_joint3 =sim.simxGetObjectHandle(clientID,"P_Arm_joint3",sim.simx_opmode_blocking)
    print(P_Arm_joint2)
    ec, p_Arm_c =sim.simxGetObjectHandle(clientID,"P_Arm_connection",sim.simx_opmode_blocking)
    print("--------------------------------------------------")
    print (p_Arm_c)
    print (ec)
    sim.simxSetJointPosition(clientID,P_Arm_joint2,180*math.pi/180,sim.simx_opmode_blocking)
    sim.simxSetJointPosition(clientID,P_Arm_joint3,180*math.pi/180,sim.simx_opmode_blocking)
    #sim.simxGetObjectPosition()
    time.sleep(3)
    col =sim.simxCheckCollision(clientID,P_Arm,flr,sim.simx_opmode_blocking)
    col2 =sim.simxCheckCollision(clientID,p_Arm_c,-2,sim.simx_opmode_blocking)
    print (col)
    print (col2)
    time.sleep(3)




    sim.simxSetJointPosition(clientID,P_Arm_joint2,0*math.pi/180,sim.simx_opmode_blocking)
    col =sim.simxCheckCollision(clientID,P_Arm,flr,sim.simx_opmode_blocking)
    print (col)
    loc =sim.simxGetObjectPosition(clientID,p_Arm_c, P_Arm,  sim.simx_opmode_blocking)
    print ("LOC ")
    print (loc)


    
    # Now try to retrieve data in a blocking fashion (i.e. a service call):
    res,objs=sim.simxGetObjects(clientID,sim.sim_handle_all,sim.simx_opmode_blocking)
    if res==sim.simx_return_ok:
        print ('Number of objects in the scene: ',len(objs))
    else:
        print ('Remote API function call returned with error code: ',res)

    time.sleep(2)
    
    # Now retrieve streaming data (i.e. in a non-blocking fashion):
    startTime=time.time()
    sim.simxGetIntegerParameter(clientID,sim.sim_intparam_mouse_x,sim.simx_opmode_streaming) # Initialize streaming
    while time.time()-startTime < 0:
        returnCode,data=sim.simxGetIntegerParameter(clientID,sim.sim_intparam_mouse_x,sim.simx_opmode_buffer) # Try to retrieve the streamed data
        if returnCode==sim.simx_return_ok: # After initialization of streaming, it will take a few ms before the first value arrives, so check the return code
            print ('Mouse position x: ',data) # Mouse position x is actualized when the cursor is over CoppeliaSim's window
        time.sleep(0.005)

    # Now send some data to CoppeliaSim in a non-blocking fashion:
    sim.simxAddStatusbarMessage(clientID,'Hello CoppeliaSim!',sim.simx_opmode_oneshot)

    # Before closing the connection to CoppeliaSim, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
    sim.simxGetPingTime(clientID)

    # Now close the connection to CoppeliaSim:
    sim.simxFinish(clientID)
else:
    print ('Failed connecting to remote API server')
print ('Program ended')
