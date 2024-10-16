# from threading import Thread
# from queue import Queue
# import random
# from Color import print_message


# #TODO  get from gun queue 


# #ACTIONS = ["shoot", "shield", "bomb", "reload", "basket", "soccer", "volley", "bowl"] 


# #ACTIONS = ["bomb", "reload", "basket", "soccer", "volley", "bowl", "shield", "gun"]
# ACTIONS = ["bomb", "basket"] #, "shield", "gun"]


# player_data = {
#     'playerID': 1,
#     'accel': [0.1, 0.2, 0.3],
#     'gyro': [0.01, 0.02, 0.03],
#     'isFire': True, #if this is true dont sent AI IMU data 
#     'isHit': False
# }

# class AI(Thread):
#     def __init__(self,IMU_queue,phone_action_queue,fire_queue):
#         Thread.__init__(self)
#         self.IMU_queue = IMU_queue
#         self.fire_queue = fire_queue  
#         self.phone_action_queue = phone_action_queue
    
#     def run(self):
#       while True:
#         message = self.IMU_queue.get()
#         # get from fire_queue.get()
#         print_message('AI Thread',f"Received '{message}' from RelayServer")
#         print()
#         #action = "bomb"

#         # TO ADD

#         action = self.random_action()
#         combined_action = action + ":1"
#         self.phone_action_queue.put(combined_action)
        

#     def random_action(self):
#       return random.choice(ACTIONS)
  
from threading import Thread
import queue
from pynq import Overlay
import pandas as pd
from AIPredictor import predict_model
import random 

#from Color import print_message

#ACTIONS = ["shoot", "shield", "bomb", "reload", "basket", "soccer", "volley", "bowl"] 
#TODO Figure out eval server for non AI actions 


#format to send out = action + ":player_id" 

ACTIONS = ["basket", "soccer", "volley", "bowl", "bomb", "shield", "reload"]

class AI(Thread):
    
    bitstream_path = "/home/xilinx/BITSTREAM/design_1.bit"
    overlay = Overlay(bitstream_path)
    predictor = predict_model(overlay)

    def __init__(self,IMU_queue,phone_action_queue,fire_queue):
        Thread.__init__(self)
        self.IMU_queue = IMU_queue
        self.fire_queue = fire_queue  
        self.phone_action_queue = phone_action_queue
    
    #def detectAction(self, message):
    #    if LOWERTHRESHOLD <= message['gyro'][0] <= UPPERTHRESHOLD and LOWERTHRESHOLD <= message['gyro'][1] <= UPPERTHRESHOLD and LOWERTHRESHOLD <= message['gyro'][2] <= UPPERTHRESHOLD:
    #        return True
    #    return False
    def random_action(self):
      return random.choice(ACTIONS)
     
    def run(self):
      messages_IMU = []
      bitstream_path = "/home/xilinx/BITSTREAM/design_1.bit"
      #overlay = Overlay(bitstream_path)
      #model = predict_model(overlay)
      while True:
        try:
            message_IMU = self.IMU_queue.get(timeout=0.5) #get from Shoot_queue
            print("Received item from IMU queue")
        except queue.Empty:
            message_IMU = None
            print("NO item received as IMU queue is empty")

        try:
            message_Shoot = self.fire_queue.get(timeout=0.5) #get from Shoot_queue
            print("Received item from fire queue")
        except queue.Empty:
            message_Shoot = None
            print("NO item received as fire queue is empty")
        
        if message_Shoot is not None and message_Shoot['isShot']: #only care abt is fired and not is hit
           action = 'gun'
           number = 1
           combined_action = f"{{'playerID': '{number}', 'action': {action}}}"
           self.phone_action_queue.put(combined_action) 
        
        if len(messages_IMU) < 20 and message_IMU is not None:
            messages_IMU.append(message_IMU)
            if len(messages_IMU) == 20: #and ~message_Shoot['isFire']:
                data_IMU = {
                    'Accel X': [message['accel'][0] for message in messages_IMU],
                    'Accel Y': [message['accel'][1] for message in messages_IMU],
                    'Accel Z': [message['accel'][2] for message in messages_IMU],
                    'Gyro X': [message['gyro'][0] for message in messages_IMU],
                    'Gyro Y': [message['gyro'][1] for message in messages_IMU],
                    'Gyro Z': [message['gyro'][2] for message in messages_IMU],
                }
                df = pd.DataFrame(data_IMU)
                action = self.random_action()
                #action = ACTIONS[model.get_action(df) - 1]
                number = 1 #Check again for this part
                combined_action = action + ":1"
                self.phone_action_queue.put(combined_action)
                #message_Shoot['isFire'] = False
                messages_IMU = []


    
    
    
