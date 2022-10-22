import math


class IKUD():
    L0 = 0
    L1 = 13 # Leg
    L2 = 16 # Feet
    A = 0 # Feet-ground angle
    B = 0 # Feet-shoulder angle 
    C = 0 # Feet-leg angle
    
    def input_height(self):
        self.L0 = float(input("Input the height: "))
        return self.L0
    
    def calculate_angle(self, L0):
        # returns value in radians
        self.B = math.acos((L0**2 + self.L1**2 - self.L2**2) / (2*self.L1*L0))
        self.C = math.acos((self.L1**2 + self.L2**2 - L0**2) / (2*self.L1*self.L2))
        
        # turns from radians to degrees
        self.B = int(self.B * (180/math.pi) + 70)
        self.C = int(self.C * (180/math.pi))
        
        print(self.B, self.C)
        return self.B, self.C