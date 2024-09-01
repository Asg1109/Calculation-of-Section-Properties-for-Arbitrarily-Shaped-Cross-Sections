from tabulate import tabulate

from math import acos , sin, cos, sqrt, pi
from numpy import linspace
import matplotlib.pyplot as plt

from regula_falsi_method import REGULA_FALSI_METHOD

class Point:
   def __init__(self,x=None,y=None,type="boundary"):
      self.name = "Point"
      self.type = type #"boundary", "centre"
      self.x = x
      self.y = y
   def __str__(self):
      return f"{self.name}(x,y) = ({self.x},{self.y})"

   def input(self):
      prompt=" Enter float/integer value : "
      show_prompt_again = 0
      print("Enter x : ",end ="")
      while True: 
         try: 
               x = float(input()) 
               break
         except: 
               if show_prompt_again == 1:
                  print(f"{prompt}",end = "")
               pass
      print("Enter y : ",end ="")
      while True: 
         try: 
               y = float(input()) 
               break
         except: 
               if show_prompt_again == 1:
                  print(f"{prompt}",end = "")
               pass

      self.x = x 
      self.y = y


class Line:

   def __init__(self, point1=None, point2=None):
      self.name = "Line"
      self.point1 = point1 
      self.point2 = point2 
   
   def __str__(self):
      table = [[f"{self.name}","x","y"],["point 1",self.point1.x,f"{self.point1.y}"],["point 2",self.point2.x,self.point2.y]]
      return tabulate(table,tablefmt="simple_grid")

   def slope(self):
      x1 = self.point1.x  
      y1 = self.point1.y
      x2 = self.point2.x  
      y2 = self.point2.y
      slope = (y2-y1)/(x2-x1)
      return slope
   def length(self):
      x1 = self.point1.x  
      y1 = self.point1.y
      x2 = self.point2.x  
      y2 = self.point2.y
      slope = sqrt((x2-x1)**2 + (y2-y1)**2)

   def area(self):
      x1=self.point1.x
      y1=self.point1.y
      x2=self.point2.x
      y2=self.point2.y
      area=1/2*(x1*y2-x2*y1)
      return area
 
   def FMOA(self, xm=0, ym=0):
      x1=self.point1.x - xm
      y1=self.point1.y - ym
      x2=self.point2.x - xm
      y2=self.point2.y - ym
      FMOA_x=x1*y1*y2/6 + x1*y2**2/6 - x2*y1**2/6 - x2*y1*y2/6
      FMOA_y=x1**2*y2/6 - x1*x2*y1/6 + x1*x2*y2/6 - x2**2*y1/6
      return FMOA_x, FMOA_y
   
   def SMOA(self, xm,ym):
      x1=self.point1.x - xm
      y1=self.point1.y - ym
      x2=self.point2.x - xm
      y2=self.point2.y - ym
      Ixx = x1*y1**2*y2/12 + x1*y1*y2**2/12 + x1*y2**3/12 - x2*y1**3/12 - x2*y1**2*y2/12 - x2*y1*y2**2/12
      Iyy = x1**3*y2/12 - x1**2*x2*y1/12 + x1**2*x2*y2/12 - x1*x2**2*y1/12 + x1*x2**2*y2/12 - x2**3*y1/12
      return Ixx, Iyy

   def x_if_y_is_known(self, yb):
      x1 = self.point1.x  
      y1 = self.point1.y  
      x2 = self.point2.x  
      y2 = self.point2.y

      xb = x1 + (x2-x1)*(yb-y1)/(y2-y1)
      
      if ((y2<=yb and yb<=y1) or (y1<=yb and yb<=y2)) and ((x2<=xb and xb<=x1) or (x1<=xb and xb<=x2)): 
         return xb
      else:
         return None
        
   def y_if_x_is_known(self, xb):
      x1 = self.point1.x  
      y1 = self.point1.y  
      x2 = self.point2.x  
      y2 = self.point2.y
      yb = y1 + (y2-y1)*(xb-x1)/(x2-x1)  
      if (((x2<=xb and xb<=x1) or (x1<=xb and xb<=x2))) and ((y2<=yb and yb<=y1) or (y1<=yb and yb<=y2)):
         return yb
      else:
         return None          
  
   def divide_shape_about_xx_axis(self,y):
      y1 = self.point1.y  
      y2 = self.point2.y
     
      if (y1>y and y2>y) or (y1==y and y2 >=y) or (y1>=y and y2==y): 
         return [[],[self]]
      elif (y1<y and y2<y) or (y1==y and y2 <=y) or (y1<y and y2==y):
         return [[self],[]]
      else:
         x = self.x_if_y_is_known(y)
         if (y1<y and y2>y):
            return [[Line(self.point1,Point(x,y))],[Line(Point(x,y),self.point2)]]
         else: # (y1>y and y2<y)
            return [[Line(Point(x,y),self.point2)],[Line(self.point1,Point(x,y))]]
         
   def divide_shape_about_yy_axis(self,x):
      x1 = self.point1.x  
      x2 = self.point2.x

      if (x1>x and x2>x) or (x1==x and x2 >=x) or (x1>=x and x2==x): 
         return [[],[self]]
      elif (x1<x and x2<x) or (x1==x and x2 <=x) or (x1<x and x2==x):
         return [[self],[]]
      else:
         y = self.y_if_x_is_known(x)
         if (x1<x and x2>x):
            return [[Line(self.point1,Point(x,y))],[Line(Point(x,y),self.point2)]]
         else: # (x1>x and x2<x)
            return [[Line(Point(x,y),self.point2)],[Line(self.point1,Point(x,y))]]

class C_curve:
   def __init__(self, point1=None, point2=None, centre=None):
      self.name = "C_curve"
      self.point1 = point1 
      self.point2 = point2 
      self.centre = centre
   def __str__(self):
      data = [[f"{self.name}","x","y"],["point 1",self.point1.x,self.point1.y],["point 2",self.point2.x,self.point2.y],["centre",self.centre.x,self.centre.y]]
      table= tabulate(data,tablefmt="simple_grid",floatfmt=".4f")

      return table
   
   def radius(self):
      xc = self.centre.x  
      yc = self.centre.y
      x1 = self.point1.x  
      y1 = self.point1.y
      radius = sqrt((x1-xc)**2 + (y1-yc)**2)
      return radius
   def central_angle(self):
      xc = self.centre.x  
      yc = self.centre.y
      x1 = self.point1.x  
      y1 = self.point1.y
      x2 = self.point2.x  
      y2 = self.point2.y
      chord_length = sqrt((x2-x1)**2 + (y2-y1)**2)
      radius = sqrt((x1-xc)**2 + (y1-yc)**2)
      cos_theta = 1 - chord_length**2/(2*radius**2)
      theta = acos(cos_theta)
      return theta
   
   def angle1(self): 
      # angle of line from centre to point1
      xc = self.centre.x  
      yc = self.centre.y
      x1 = self.point1.x  
      y1 = self.point1.y
      r = sqrt((x1-xc)**2 + (y1-yc)**2)

      if y1-yc>=0:
         theta1=acos((x1-xc)/r)
      else:
         theta1 = 2*pi - acos((x1-xc)/r)    
      return theta1
   def angle2(self): 
      # angle of line from centre to point1
      xc = self.centre.x  
      yc = self.centre.y
      x2 = self.point2.x  
      y2 = self.point2.y
      r = sqrt((x2-xc)**2 + (y2-yc)**2)
      if y2-yc>=0:
         theta2=acos((x2-xc)/r)
      else:
         theta2 = 2*pi-1*acos((x2-xc)/r)

      return theta2
   def angle(self):
      theta1=self.angle1()
      theta2=self.angle2()

      if (theta1-theta2) > pi:
         theta1 = theta1- 2*pi
      elif (theta2 -theta1)> pi:
         theta2 = theta2 - 2*pi
      return theta1, theta2

   def points(self):
      xpoints=[]
      ypoints=[]
      try:
         xc=self.centre.x 
         yc=self.centre.y
         r=self.radius()
         theta1, theta2 = self.angle()
         theta_space=linspace(theta1,theta2,num=50)
         for theta in theta_space:
            xpoints.append(xc+r*cos(theta))
            ypoints.append(yc+r*sin(theta))
      except:
         pass
      return xpoints, ypoints
   
   def area(self):
      xc=self.centre.x
      yc=self.centre.y
      r=self.radius()
      theta1,theta2 = self.angle()
      area=r*(-r*theta1 + r*theta2 - xc*sin(theta1) + xc*sin(theta2) + yc*cos(theta1) - yc*cos(theta2))/2
      return area
   
   def FMOA(self,xm=0,ym=0):
      xc=self.centre.x - xm
      yc=self.centre.y - ym
      r=self.radius()
      theta1,theta2 = self.angle()
      FMOA_x=r*(2*r**2*cos(theta1) - 2*r**2*cos(theta2) - 3*r*theta1*yc + 3*r*theta2*yc + r*xc*cos(2*theta1)/2 - r*xc*cos(2*theta2)/2 + r*yc*sin(2*theta1)/2 - r*yc*sin(2*theta2)/2 - 2*xc*yc*sin(theta1) + 2*xc*yc*sin(theta2) + 2*yc**2*cos(theta1) - 2*yc**2*cos(theta2))/6
      FMOA_y=r*(-2*r**2*sin(theta1) + 2*r**2*sin(theta2) - 3*r*theta1*xc + 3*r*theta2*xc - r*xc*sin(2*theta1)/2 + r*xc*sin(2*theta2)/2 + r*yc*cos(2*theta1)/2 - r*yc*cos(2*theta2)/2 - 2*xc**2*sin(theta1) + 2*xc**2*sin(theta2) + 2*xc*yc*cos(theta1) - 2*xc*yc*cos(theta2))/6
      return FMOA_x, FMOA_y
   
   def SMOA(self,xm,ym):
  
      xc=self.centre.x - xm
      yc=self.centre.y - ym
      r=self.radius()
      theta1,theta2 = self.angle()
      Ixx = r*(-3*r**3*theta1 + 3*r**3*theta2 + 3*r**3*sin(2*theta1)/2 - 3*r**3*sin(2*theta2)/2 - 3*r**2*xc*sin(theta1)/2 + r**2*xc*sin(3*theta1)/2 + 3*r**2*xc*sin(theta2)/2 - r**2*xc*sin(3*theta2)/2 + 33*r**2*yc*cos(theta1)/2 - r**2*yc*cos(3*theta1)/2 - 33*r**2*yc*cos(theta2)/2 + r**2*yc*cos(3*theta2)/2 - 12*r*theta1*yc**2 + 12*r*theta2*yc**2 + 3*r*xc*yc*cos(2*theta1) - 3*r*xc*yc*cos(2*theta2) + 3*r*yc**2*sin(2*theta1) - 3*r*yc**2*sin(2*theta2) - 6*xc*yc**2*sin(theta1) + 6*xc*yc**2*sin(theta2) + 6*yc**3*cos(theta1) - 6*yc**3*cos(theta2))/24
      Iyy=r*(-3*r**3*theta1 + 3*r**3*theta2 - 3*r**3*sin(2*theta1)/2 + 3*r**3*sin(2*theta2)/2 - 33*r**2*xc*sin(theta1)/2 - r**2*xc*sin(3*theta1)/2 + 33*r**2*xc*sin(theta2)/2 + r**2*xc*sin(3*theta2)/2 + 3*r**2*yc*cos(theta1)/2 + r**2*yc*cos(3*theta1)/2 - 3*r**2*yc*cos(theta2)/2 - r**2*yc*cos(3*theta2)/2 - 12*r*theta1*xc**2 + 12*r*theta2*xc**2 - 3*r*xc**2*sin(2*theta1) + 3*r*xc**2*sin(2*theta2) + 3*r*xc*yc*cos(2*theta1) - 3*r*xc*yc*cos(2*theta2) - 6*xc**3*sin(theta1) + 6*xc**3*sin(theta2) + 6*xc**2*yc*cos(theta1) - 6*xc**2*yc*cos(theta2))/24
   
      return Ixx, Iyy


   def x_if_y_is_known(self, yb):
      x1 = self.point1.x  
      y1 = self.point1.y
      x2 = self.point2.x  
      y2 = self.point2.y
      xc = self.centre.x  
      yc = self.centre.y
      r = self.radius()

      xb=[]
      if abs(yb-yc)<=r :
         # print('1 if abs(yb-yc)<=r :')
         xb1 = xc + sqrt(r**2-(yb-yc)**2)
         xb2 = xc - sqrt(r**2-(yb-yc)**2)
         
         pb1=Point(xb1,yb)
         pb2=Point(xb2,yb)
         if ( ((y1>=yc and y2>yc) or (y1>yc and y2>=yc)) and yb>=yc ) or ( ((y1<=yc and y2<yc) or (y1<yc and y2<=yc)) and yb<=yc ):
            # print('11 if ( ((y1>=yc and y2>yc) or (y1>yc and y2>=yc)) and yb>=yc ) or ( ((y1<=yc and y2<yc) or (y1>yc and y2>=yc)) and yb<=yc ):')
            
            if (x2<=xb1 and xb1<=x1) or (x1<=xb1 and xb1<=x2):
               # print('111 if (x2<=xb1 and xb1<=x1) or (x1<=xb1 and xb1<=x1):')
               xb.append(xb1)
               if xb1==xb2:
                  # print('1111 if (x2<=xb1 and xb1<=x1) or (x1<=xb1 and xb1<=x1):')
                  return xb
            if (x2<=xb2 and xb2<=x1) or (x1<=xb2 and xb2<=x2):
               # print('112 (x2<=xb2 and xb2<=x1) or (x1<=xb2 and xb2<=x1):')

               xb.append(xb2)
         elif (y1<yc and y2>yc) or (y1>yc and y2<yc):
            # print('12 (y1<yc and y2>yc) or (y1>yc and y2<yc)')
            if (x1>=xc and x2>((xc-(x1-xc)))) or (x2>=xc and x1>((xc-(x2-xc)))):
               # print('121 (x1>=xc and x2>((xc-(x1-xc)))) or (x2>=xc and x1>((xc-(x2-xc)))):')
               if yb>=yc:
                  # print('121 if yb>=yc:')
                  if y1<yc: # y2>yc
                     # print('1211 if y1<yc:')
                     if xb1>=x2:
                        # print('12111 if xb1>=x2:')
                        xb.append(xb1)
                        if xb1==xb2:
                           # print('121111 if xb1==xb2:')
                           return xb
                     if xb2>=x2:
                        # print('12112 if xb1>=x2:')
                        xb.append(xb2)
                        return xb
                  else: #y1>yc
                     # print('1212 if y1<yc:')
                     if xb1>=x1:
                        # print('12121 if xb1>=x2:')
                        xb.append(xb1)
                        if xb1==xb2:
                           # print('121211 if xb1>=x2:')
                           return xb
                     if xb2>=x1:
                        # print('12122 if xb1>=x2:')
                        xb.append(xb2)
                        return xb
               else: # yb<yc
                  if y1<yc: # y2>yc
                     if xb1>=x1:
                        xb.append(xb1)
                        if xb1==xb2:
                           return xb
                     if xb2>=x1:
                        xb.append(xb2)
                        return xb
                  else: #y1>yc y2<yc
                     if xb1>=x2:
                        xb.append(xb1)
                        if xb1==xb2:
                           return xb
                     if xb2>=x2:
                        xb.append(xb2)
                        return xb

            elif (x1<=xc and x2<((xc+(xc-x1)))) or (x2<=xc and x1<((xc+(xc-x2)))):
               if yb>=yc:
                  if y1<yc: # y2>yc
                     if xb1<=x2:
                        xb.append(xb1)
                        if xb1==xb2:
                           return xb
                     if xb2<=x2:
                        xb.append(xb2)
                        return xb
                  else: #y1>yc
                     if xb1<=x1:
                        xb.append(xb1)
                        if xb1==xb2:
                           return xb
                     if xb2<=x1:
                        xb.append(xb2)
                        return xb
               else: # yb<yc
                  if y1<yc: # y2>yc
                     if xb1<=x1:
                        xb.append(xb1)
                        if xb1==xb2:
                           return xb
                     if xb2<=x1:
                        xb.append(xb2)
                        return xb
                  else: #y1>yc y2<yc
                     if xb1<=x2:
                        xb.append(xb1)
                        if xb1==xb2:
                           return xb
                     if xb2<=x2:
                        xb.append(xb2)
                        return xb

            
      return xb
               

   def y_if_x_is_known(self, xb):
      x1 = self.point1.x  
      y1 = self.point1.y
      x2 = self.point2.x  
      y2 = self.point2.y
      xc = self.centre.x  
      yc = self.centre.y
      r = self.radius()

      yb=[]
      if abs(xb-yc)<=r :
         # print('1 if abs(xb-yc)<=r :')
         yb1 = xc + sqrt(r**2-(xb-yc)**2)
         yb2 = xc - sqrt(r**2-(xb-yc)**2)
         
         pb1=Point(yb1,xb)
         pb2=Point(yb2,xb)
         if ( ((x1>=yc and x2>yc) or (x1>yc and x2>=yc)) and xb>=yc ) or ( ((x1<=yc and x2<yc) or (x1<yc and x2<=yc)) and xb<=yc ):
            # print('11 if ( ((x1>=yc and x2>yc) or (x1>yc and x2>=yc)) and xb>=yc ) or ( ((x1<=yc and x2<yc) or (x1>yc and x2>=yc)) and xb<=yc ):')
            
            if (y2<=yb1 and yb1<=y1) or (y1<=yb1 and yb1<=y2):
               # print('111 if (y2<=yb1 and yb1<=y1) or (y1<=yb1 and yb1<=y1):')
               yb.append(yb1)
               if yb1==yb2:
                  # print('1111 if (y2<=yb1 and yb1<=y1) or (y1<=yb1 and yb1<=y1):')
                  return yb
            if (y2<=yb2 and yb2<=y1) or (y1<=yb2 and yb2<=y2):
               # print('112 (y2<=yb2 and yb2<=y1) or (y1<=yb2 and yb2<=y1):')

               yb.append(yb2)
         elif (x1<yc and x2>yc) or (x1>yc and x2<yc):
            # print('12 (x1<yc and x2>yc) or (x1>yc and x2<yc)')
            if (y1>=xc and y2>((xc-(y1-xc)))) or (y2>=xc and y1>((xc-(y2-xc)))):
               # print('121 (y1>=xc and y2>((xc-(y1-xc)))) or (y2>=xc and y1>((xc-(y2-xc)))):')
               if xb>=yc:
                  # print('121 if xb>=yc:')
                  if x1<yc: # x2>yc
                     # print('1211 if x1<yc:')
                     if yb1>=y2:
                        # print('12111 if yb1>=y2:')
                        yb.append(yb1)
                        if yb1==yb2:
                           # print('121111 if yb1==yb2:')
                           return yb
                     if yb2>=y2:
                        # print('12112 if yb1>=y2:')
                        yb.append(yb2)
                        return yb
                  else: #x1>yc
                     # print('1212 if x1<yc:')
                     if yb1>=y1:
                        # print('12121 if yb1>=y2:')
                        yb.append(yb1)
                        if yb1==yb2:
                           # print('121211 if yb1>=y2:')
                           return yb
                     if yb2>=y1:
                        # print('12122 if yb1>=y2:')
                        yb.append(yb2)
                        return yb
               else: # xb<yc
                  if x1<yc: # x2>yc
                     if yb1>=y1:
                        yb.append(yb1)
                        if yb1==yb2:
                           return yb
                     if yb2>=y1:
                        yb.append(yb2)
                        return yb
                  else: #x1>yc x2<yc
                     if yb1>=y2:
                        yb.append(yb1)
                        if yb1==yb2:
                           return yb
                     if yb2>=y2:
                        yb.append(yb2)
                        return yb

            elif (y1<=xc and y2<((xc+(xc-y1)))) or (y2<=xc and y1<((xc+(xc-y2)))):
               if xb>=yc:
                  if x1<yc: # x2>yc
                     if yb1<=y2:
                        yb.append(yb1)
                        if yb1==yb2:
                           return yb
                     if yb2<=y2:
                        yb.append(yb2)
                        return yb
                  else: #x1>yc
                     if yb1<=y1:
                        yb.append(yb1)
                        if yb1==yb2:
                           return yb
                     if yb2<=y1:
                        yb.append(yb2)
                        return yb
               else: # xb<yc
                  if x1<yc: # x2>yc
                     if yb1<=y1:
                        yb.append(yb1)
                        if yb1==yb2:
                           return yb
                     if yb2<=y1:
                        yb.append(yb2)
                        return yb
                  else: #x1>yc x2<yc
                     if yb1<=y2:
                        yb.append(yb1)
                        if yb1==yb2:
                           return yb
                     if yb2<=y2:
                        yb.append(yb2)
                        return yb

            
      return yb
   def divide_shape_about_xx_axis(self,y):
      # print("divide_shape_above_xx_axis")
      y1 = self.point1.y
      y2 = self.point2.y  
      yc = self.centre.y
      x_list=self.x_if_y_is_known(y)
      # print(len(x_list))
      if len(x_list)==0: # number of times C_Curve crossed above y
         # print("if1")
         if y1>y and y2>y:
            # print("if11")
            return [[],[self]]
         else:
            # print("else12")
            return [[self],[]]
      elif len(x_list)==1:
         # print("elif2")
         if (y1==y and y2>y) or (y2==y and y1>y) :
            # print("if21")
            return [[],[self]]
         elif (y1==y and y2<y) or (y2==y and y1<y):
            # print("elif22")
            return [[self],[]]
         else:
            # print("else23")
            if (y1<y and y2>y):
               # print("if231")
               return [[C_curve(self.point1,Point(x_list[0],y),self.centre)],
                       [C_curve(Point(x_list[0],y),self.point2,self.centre)]]
            else: # (y1>y and y2<y)
               # print("if232")
               return [[C_curve(Point(x_list[0],y),self.point2,self.centre)],
                       [C_curve(self.point1,Point(x_list[0],y),self.centre)]]
      else:
         # print("else3")
         if y1==y and y2==y and yc <y:
            # print("if31")
            return [[],[self]]
         elif y1==y and y2 == y and yc >y:
            # print("elif32")
            return [self,[]]
         else:
            # print("else33")
            if y1==y and yc<y:
               # print("if331")
               return [[Line(self.point1,Point(x_list[1],y)), C_curve(Point(x_list[1],y),self.point2,self.centre)],
                       [C_curve(self.point1,Point(x_list[1],y),self.centre)]]
            elif y1==y and yc>y:
               # print("elif332")
               return [[C_curve(self.point1,Point(x_list[1],y),self.centre)],
                       [Line(self.point1,Point(x_list[1],y)), C_curve(Point(x_list[1],y),self.point2,self.centre)]]
            elif y2==y and yc<y:
               # print("elif333")
               return [ [C_curve(self.point1,Point(x_list[0],y),self.centre), Line(Point(x_list[0],y),self.point2)],
                        [C_curve(Point(x_list[0],y),self.point2,self.centre)]]
            elif y2==y and yc>y:
               # print("elif334")
               return [ [C_curve(Point(x_list[0],y),self.point2,self.centre)],
                        [C_curve(self.point1,Point(x_list[0],y),self.centre), Line(Point(x_list[0],y),self.point2)]]
            elif yc<y:
               # print("elif335")
               return [[C_curve(self.point1,Point(x_list[0],y),self.centre), Line(Point(x_list[0],y),Point(x_list[1],y)),C_curve(Point(x_list[1],y),self.point2,self.centre)],
                       [C_curve(Point(x_list[0],y),Point(x_list[1],y),self.centre)]]
            else: # yc>y
               # print("else336")
               return [[C_curve(Point(x_list[0],y),Point(x_list[1],y),self.centre)],
                       [C_curve(self.point1,Point(x_list[0],y),self.centre), Line(Point(x_list[0],y),Point(x_list[1],y)),C_curve(Point(x_list[1],y),self.point2,self.centre)]]

   def divide_shape_about_yy_axis(self,x):
      x1 = self.point1.x
      x2 = self.point2.x  
      xc = self.centre.x
      y_list=self.y_if_x_is_known(x)
      if len(y_list)==0: # number of times C_Curve crossed above x
         # print("if1")
         if x1>x and x2>x:
            # print("if11")
            return [[],[self]]
         else:
            # print("else12")
            return [[self],[]]
      elif len(y_list)==1:
         # print("elif2")
         if (x1==x and x2>x) or (x2==x and x1>x) :
            # print("if21")
            return [[],[self]]
         elif (x1==x and x2<x) or (x2==x and x1<x):
            # print("elif22")
            return [[self],[]]
         else:
            # print("else23")
            if (x1<x and x2>x):
               # print("if231")
               return [[C_curve(self.point1,Point(x,y_list[0]),self.centre)],
                       [C_curve(Point(x,y_list[0]),self.point2,self.centre)]]
            else: # (x1>x and x2<x)
               # print("if232")
               return [[C_curve(Point(x,y_list[0]),self.point2,self.centre)],
                       [C_curve(self.point1,Point(x,y_list[0]),self.centre)]]
      else:
         # print("else3")
         if x1==x and x2==x and xc <x:
            # print("if31")
            return [[],[self]]
         elif x1==x and x2 == x and xc >x:
            # print("elif32")
            return [self,[]]
         else:
            # print("else33")
            if x1==x and xc<x:
               # print("if331")
               return [[Line(self.point1,Point(x,y_list[1])), C_curve(Point(x,y_list[1]),self.point2,self.centre)],
                       [C_curve(self.point1,Point(x,y_list[1]),self.centre)]]
            elif x1==x and xc>x:
               # print("elif332")
               return [[C_curve(self.point1,Point(x,y_list[1]),self.centre)],
                       [Line(self.point1,Point(x,y_list[1])), C_curve(Point(x,y_list[1]),self.point2,self.centre)]]
            elif x2==x and xc<x:
               # print("elif333")
               return [ [C_curve(self.point1,Point(x,y_list[0]),self.centre), Line(Point(x,y_list[0]),self.point2)],
                        [C_curve(Point(x,y_list[0]),self.point2,self.centre)]]
            elif x2==x and xc>x:
               # print("elif334")
               return [ [C_curve(Point(x,y_list[0]),self.point2,self.centre)],
                        [C_curve(self.point1,Point(x,y_list[0]),self.centre), Line(Point(x,y_list[0]),self.point2)]]
            elif xc<x:
               # print("elif335")
               return [[C_curve(self.point1,Point(x,y_list[0]),self.centre), Line(Point(x,y_list[0]),Point(x,y_list[1])),C_curve(Point(x,y_list[1]),self.point2,self.centre)],
                       [C_curve(Point(x,y_list[0]),Point(x,y_list[1]),self.centre)]]
            else: # xc>x
               # print("else336")
               return [[C_curve(Point(x,y_list[0]),Point(x,y_list[1]),self.centre)],
                       [C_curve(self.point1,Point(x,y_list[0]),self.centre), Line(Point(x,y_list[0]),Point(x,y_list[1])),C_curve(Point(x,y_list[1]),self.point2,self.centre)]]


class Shape:
   def __init__(self, point_list=[], line_list=[]):
      self.name="Shape"
      self.points=point_list
      self.lines=self.sort_line(line_list) # includes lines,curves

   def __str__(self):
      point_list=[]
      line_list=[]
      for point in self.points:
         point_list.append([point]) 
      for line in self.lines:
         line_list.append([line]) 

      table1=tabulate(point_list,tablefmt='plain')

      table2=tabulate(line_list,tablefmt='plain')
      data = [[f"S{self.name}"],[table1],[table2]]
      
      table = tabulate(data,tablefmt="plain")
      return table

   def sort_line(self, line_list):
      new_lines=[line_list[0]]
      p2=line_list[0].point2
      line_list.remove(line_list[0])
      while len(line_list)>0:
         flag = True
         for line2 in line_list:
            if line2.point1 == p2:
               new_lines.append(line2)
               p2=line2.point2
               line_list.remove(line2)
               flag = False
               
         if flag==True and len(line_list)>1:
            new_lines.append(line_list[0])
            p2 = line_list[0].point2
            line_list.remove(line_list[0])
         if len(line_list)==1:
            new_lines.append(line_list[0])
            line_list.remove(line_list[0])
      return new_lines
   
   def area(self):
      area = 0
      for line in self.lines:
         area=area + line.area()
      return area
   def centroid(self):
      area = abs(self.area())
      FMOA_x=0
      FMOA_y=0
      for line in self.lines:
         FMOA_x = FMOA_x + line.FMOA(0,0)[0]
         FMOA_y = FMOA_y + line.FMOA(0,0)[1]
      x_centroid = FMOA_y/area
      y_centroid = FMOA_x/area
      return x_centroid,y_centroid
   
   def FMOA(self, x, y):
      FMOA_x = 0
      FMOA_y = 0
      for line in self.lines:
         FMOA_x = FMOA_x + line.FMOA(x,y)[0]
         FMOA_y = FMOA_y + line.FMOA(x,y)[1]
      return FMOA_x, FMOA_y
   def SMOA(self, x, y):
      SMOA_x = 0
      SMOA_y = 0
      for line in self.lines:
         SMOA_x = SMOA_x + line.SMOA(x,y)[0]
         SMOA_y = SMOA_y + line.SMOA(x,y)[1]
      return SMOA_x, SMOA_y
   def radius_of_gyration(self):
      Ixx,Iyy = self.inertia()
      area = self.area()
      rxx = sqrt(Ixx/area)
      ryy = sqrt(Iyy/area)
   def inertia(self):
      # SMOA : Second Moment of Area
      Ixx=0
      Iyy=0
      xm,ym=self.centroid()
      for line in self.lines:
         Ixx = Ixx + line.SMOA(xm,ym)[0]
         Iyy = Iyy + line.SMOA(xm,ym)[1]
      return Ixx, Iyy
   def display(self, show=True):
      xpoints=[]
      ypoints=[]
      for line in self.lines:
         if isinstance(line,Line):
               xpoints.append(line.point1.x)
               ypoints.append(line.point1.y)
         elif isinstance(line,C_curve):
               xc=line.centre.x
               yc=line.centre.y
               r=line.radius()
               theta1, theta2 = line.angle()
               theta_space=linspace(theta1,theta2,num=50)
               for theta in theta_space:
                  xpoints.append(xc+r*cos(theta))
                  ypoints.append(yc+r*sin(theta))
      if len(xpoints)>0 and len(ypoints)>0:
         xpoints.append(xpoints[0])
         ypoints.append(ypoints[0])
         if show == True:
            fig= plt.gca()
            fig.plot(xpoints, ypoints)
            fig.set_aspect("equal")
            fig.axis("off")
            plt.show()
      return xpoints, ypoints

   def PNA(self):
      # distance of Plastic Neutral Axis
      xl,yl,xu,yu = self.extreme_coordinates()
      half_area =self.area()/2
      xp = REGULA_FALSI_METHOD(xl,xu,self.area_below_yy_axis,half_area)
      yp = REGULA_FALSI_METHOD(yl,yu,self.area_below_xx_axis,half_area)
      return xp, yp

   def extreme_coordinates(self):
      xpoints, ypoints= self.display(show=False)
      return min(xpoints), min(ypoints), max(xpoints), max(ypoints)
   
   def elastic_section_modulus(self):
      xl,yl,xu,yu = self.extreme_coordinates()
      xm,ym=self.centroid()
      Ixx,Iyy = self.inertia()
      Zexx = Ixx/(max(abs(yl-ym),abs(yu-ym)))
      Zeyy = Iyy/(max(abs(xl-xm),abs(xu-xm)))
      return Zexx, Zeyy
   
   def plastic_section_modulus(self):
      xp,yp = self.PNA()
      Zpbxx= 0
      Zpaxx= 0
      Zpbyy= 0
      Zpayy= 0
      for line in self.lines_below_xx_axis(yp):
         Zpbxx = Zpbxx + line.FMOA(xp,yp)[0]
      for line in self.lines_above_xx_axis(yp):
         Zpaxx = Zpaxx + line.FMOA(xp,yp)[0]
      Zpxx = abs(Zpbxx)+abs(Zpaxx)

      for line in self.lines_below_yy_axis(xp):
         Zpbyy = Zpbyy + line.FMOA(xp,yp)[1]
      for line in self.lines_above_yy_axis(xp):
         Zpayy = Zpayy + line.FMOA(xp,yp)[1]
      Zpyy = abs(Zpbyy)+abs(Zpayy)
      return Zpxx, Zpyy
   
   def lines_below_xx_axis(self,y):
      lines_bxx = [] # lines below xx axis
      iter = 0
      flag = True
      while iter < len(self.lines) and flag == True:
         # print("while1")
         line=self.lines[iter]
         iter=iter+1
         # print(f"iter={iter}")
         line_list=line.divide_shape_about_xx_axis(y)[0]
         if len(line_list)!=0:
               # print("if11")
               flag=False
               j=0
               while j<len(line_list):
                  # print("while11")
                  lines_bxx.append(line_list[j])
                  j=j+1

      while iter < len(self.lines):
         # print("while2")
         line=self.lines[iter]
         iter=iter+1
         # print(f"iter={iter}")
         line_list=line.divide_shape_about_xx_axis(y)[0]
         if len(line_list)>0:
               # print("if21")
               p_prev =lines_bxx[-1].point2 
               p_next = line_list[0].point1
               if p_prev!= p_next:
                  lines_bxx.append(Line(p_prev,p_next))
               j=0
               while j<len(line_list):
                  # print("while21")
                  lines_bxx.append(line_list[j])
                  j=j+1
      if len(lines_bxx)>0 and lines_bxx[-1].point2 != lines_bxx[0].point1:
         lines_bxx.append(Line(lines_bxx[-1].point2,lines_bxx[0].point1))
      return lines_bxx
   
   def lines_above_xx_axis(self,y):
      lines_axx = [] # lines below xx axis
      iter = 0
      flag = True
      while iter < len(self.lines) and flag == True:
         # print("while1")
         line=self.lines[iter]
         iter=iter+1
         # print(f"iter={iter}")
         line_list=line.divide_shape_about_xx_axis(y)[1]
         if len(line_list)!=0:
               # print("if11")
               flag=False
               j=0
               while j<len(line_list):
                  # print("while11")
                  lines_axx.append(line_list[j])
                  j=j+1

      while iter < len(self.lines):
         # print("while2")
         line=self.lines[iter]
         iter=iter+1
         # print(f"iter={iter}")
         line_list=line.divide_shape_about_xx_axis(y)[1]
         if len(line_list)>0:
               # print("if21")
               p_prev =lines_axx[-1].point2 
               p_next = line_list[0].point1
               if p_prev!= p_next:
                  lines_axx.append(Line(p_prev,p_next))
               j=0
               while j<len(line_list):
                  # print("while21")
                  lines_axx.append(line_list[j])
                  j=j+1
      if len(lines_axx)>0 and lines_axx[-1].point2 != lines_axx[0].point1:
         lines_axx.append(Line(lines_axx[-1].point2,lines_axx[0].point1))
      return lines_axx
   
   def lines_below_yy_axis(self,x):
      lines_byy = [] # lines below yy axis
      iter = 0
      flag = True
      while iter < len(self.lines) and flag == True:
         # print("while1")
         line=self.lines[iter]
         iter=iter+1
         # print(f"iter={iter}")
         line_list=line.divide_shape_about_yy_axis(x)[0]
         if len(line_list)!=0:
               # print("if11")
               flag=False
               j=0
               while j<len(line_list):
                  # print("while11")
                  lines_byy.append(line_list[j])
                  j=j+1

      while iter < len(self.lines):
         # print("while2")
         line=self.lines[iter]
         iter=iter+1
         # print(f"iter={iter}")
         line_list=line.divide_shape_about_yy_axis(x)[0]
         if len(line_list)>0:
               # print("if21")
               p_prev = lines_byy[-1].point2 
               p_next = line_list[0].point1
               if p_prev!= p_next:
                  lines_byy.append(Line(p_prev,p_next))
               j=0
               while j<len(line_list):
                  # print("while21")
                  lines_byy.append(line_list[j])
                  j=j+1
      if len(lines_byy)>0 and lines_byy[-1].point2 != lines_byy[0].point1:
         lines_byy.append(Line(lines_byy[-1].point2,lines_byy[0].point1))
      return lines_byy
   
   def lines_above_yy_axis(self,x):
      lines_ayy = [] # lines below yy axis
      iter = 0
      flag = True
      while iter < len(self.lines) and flag == True:
         # print("while1")
         line=self.lines[iter]
         iter=iter+1
         # print(f"iter={iter}")
         line_list=line.divide_shape_about_yy_axis(x)[1]
         if len(line_list)!=0:
               # print("if11")
               flag=False
               j=0
               while j<len(line_list):
                  # print("while11")
                  lines_ayy.append(line_list[j])
                  j=j+1

      while iter < len(self.lines):
         # print("while2")
         line=self.lines[iter]
         iter=iter+1
         # print(f"iter={iter}")
         line_list=line.divide_shape_about_yy_axis(x)[1]
         if len(line_list)>0:
               # print("if21")
               p_prev =lines_ayy[-1].point2 
               p_next = line_list[0].point1
               if p_prev!= p_next:
                  lines_ayy.append(Line(p_prev,p_next))
               j=0
               while j<len(line_list):
                  # print("while21")
                  lines_ayy.append(line_list[j])
                  j=j+1
      if len(lines_ayy)>0 and lines_ayy[-1].point2 != lines_ayy[0].point1:
         lines_ayy.append(Line(lines_ayy[-1].point2,lines_ayy[0].point1))
      return lines_ayy
   
   def display_shape_below_xx_axis(self, y, show=True):
      xpoints=[]
      ypoints=[]
      if len(self.lines_below_xx_axis(y))>0:
         for line in self.lines_below_xx_axis(y):
               if isinstance(line,Line):
                  xpoints.append(line.point1.x)
                  ypoints.append(line.point1.y)
               elif isinstance(line,C_curve):
                  xc=line.centre.x
                  yc=line.centre.y
                  r=line.radius()
                  theta1, theta2 = line.angle()
                  theta_space=linspace(theta1,theta2,num=50)
                  for theta in theta_space:
                     xpoints.append(xc+r*cos(theta))
                     ypoints.append(yc+r*sin(theta))

         xpoints.append(xpoints[0])
         ypoints.append(ypoints[0])
         if show==True:
            fig= plt.gca()
            fig.plot(xpoints, ypoints)
            fig.set_aspect("equal")
            fig.axis("off")
            plt.show()
      else:
         print("shape not exist")
      return xpoints, ypoints

   def display_shape_below_yy_axis(self, x, show=True):
      xpoints=[]
      ypoints=[]
      if len(self.lines_below_yy_axis(x))>0:
         for line in self.lines_below_yy_axis(x):
               if isinstance(line,Line):
                  xpoints.append(line.point1.x)
                  ypoints.append(line.point1.y)
               elif isinstance(line,C_curve):
                  xc=line.centre.x
                  yc=line.centre.y
                  r=line.radius()
                  theta1, theta2 = line.angle()
                  theta_space=linspace(theta1,theta2,num=50)
                  for theta in theta_space:
                     xpoints.append(xc+r*cos(theta))
                     ypoints.append(yc+r*sin(theta))

         xpoints.append(xpoints[0])
         ypoints.append(ypoints[0])
         if show==True:
            fig= plt.gca()
            fig.plot(xpoints, ypoints)
            fig.set_aspect("equal")
            fig.axis("off")
            plt.show()
      else:
         print("shape not exist")
      return xpoints, ypoints

   def display_shape_above_xx_axis(self, y, show=True):
      xpoints=[]
      ypoints=[]
      if len(self.lines_above_xx_axis(y))>0:
         for line in self.lines_above_xx_axis(y):
               if isinstance(line,Line):
                  xpoints.append(line.point1.x)
                  ypoints.append(line.point1.y)
               elif isinstance(line,C_curve):
                  xc=line.centre.x
                  yc=line.centre.y
                  r=line.radius()
                  theta1, theta2 = line.angle()
                  theta_space=linspace(theta1,theta2,num=50)
                  for theta in theta_space:
                     xpoints.append(xc+r*cos(theta))
                     ypoints.append(yc+r*sin(theta))

         xpoints.append(xpoints[0])
         ypoints.append(ypoints[0])
         if show==True:
            fig= plt.gca()
            fig.plot(xpoints, ypoints)
            fig.set_aspect("equal")
            fig.axis("off")
            plt.show()
      else:
         print("shape not exist")
      return xpoints, ypoints
   
   def display_shape_above_yy_axis(self, x, show=True):
      xpoints=[]
      ypoints=[]
      if len(self.lines_above_yy_axis(x))>0:
         for line in self.lines_above_yy_axis(x):
            if isinstance(line,Line):
                  xpoints.append(line.point1.x)
                  ypoints.append(line.point1.y)
            elif isinstance(line,C_curve):
                  xc=line.centre.x
                  yc=line.centre.y
                  r=line.radius()
                  theta1, theta2 = line.angle()
                  theta_space=linspace(theta1,theta2,num=50)
                  for theta in theta_space:
                     xpoints.append(xc+r*cos(theta))
                     ypoints.append(yc+r*sin(theta))

         if show==True:
            fig= plt.gca()
            fig.plot(xpoints, ypoints)
            fig.set_aspect("equal")
            fig.axis("off")
            plt.show()
      else:
         print("shape not exist")
      return xpoints, ypoints

   def area_below_xx_axis(self,y):
      if len(self.lines_below_xx_axis(y))>0:
         area = 0
         for line in self.lines_below_xx_axis(y):
               # print(line)
               area=area + line.area()
         return area
      else:
         return 0
      
   def area_below_yy_axis(self,x):
      if len(self.lines_below_yy_axis(x))>0:
         area = 0
         for line in self.lines_below_yy_axis(x):
               # print(line)
               area=area + line.area()
         return area
      else:
         return 0
   
   def area_above_xx_axis(self,y):
      if len(self.lines_above_xx_axis(y))>0:
         area = 0
         for line in self.lines_above_xx_axis(y):
               # print(line)
               area=area + line.area()
         return area
      else:
         return 0
      
   def area_above_yy_axis(self,x):
      if len(self.lines_above_yy_axis(x))>0:
         area = 0
         for line in self.lines_above_yy_axis(x):
               # print(line)
               area=area + line.area()
         return area
      else:
         return 0
      

class Geometry:
   def __init__(self, shape_list=[], unitweight=7850):
      self.name = "Geomtery"
      self.shapes = shape_list
      self.unitweight = unitweight
   
   def properties(self):
      area = self.area()
      w = area*self.unitweight/(1000*2)
      xm,ym = self.centroid()
      Ixx, Iyy =self.inertia()
      rxx,ryy = sqrt(Ixx/area), sqrt(Iyy/area)
      Zexx, Zeyy= self.elastic_section_modulus()
      xp,yp = self.PNA()
      Zpxx, Zpyy = self.plastic_section_modulus()
      return w, area, xm, ym, Ixx, Iyy, rxx, ryy, Zexx, Zeyy, xp,yp, Zpxx, Zpyy

   def area(self):
      area =0
      for shape in self.shapes:
         area = area + shape.area()
      return area
   
   def display(self, show=True):
      points_list_posv=[]
      points_list_negv=[]
      for shape in self.shapes:
         if shape.area()>0:
            points_list_posv.append(list(shape.display(show=False)))
         else:
            points_list_negv.append(list(shape.display(show=False)))
      if show==True:
         fig= plt.gca()
         for points_list in points_list_posv:
            fig.plot(points_list[0],points_list[1],color="black",linewidth = '0.7')
            fig.fill(points_list[0],points_list[1],color="#1f88d9", alpha=0.6)
         for points_list in points_list_negv:
            fig.plot(points_list[0],points_list[1],color="black",linewidth = '0.7')
            fig.fill(points_list[0],points_list[1],color="white")
            
         fig.set_aspect("equal")
         fig.axis("off")
         plt.show()
      return points_list_posv, points_list_negv
   def display_shape_below_xx_axis(self,y):
      shape_list=self.shapes_below_xx_axis(y)
      Geometry(shape_list).display()

   def display_shape_above_xx_axis(self,y):
      shape_list=self.shapes_above_xx_axis(y)
      Geometry(shape_list).display()

   def display_shape_below_yy_axis(self,x):
      shape_list=self.shapes_below_yy_axis(x)
      Geometry(shape_list).display()

   def display_shape_above_yy_axis(self,x):
      shape_list=self.shapes_above_yy_axis(x)
      Geometry(shape_list).display()

   def printproperties(self):
      w, area, xm, ym, Ixx, Iyy, rxx, ryy, Zexx, Zeyy, xp,yp, Zpxx, Zpyy =self.properties()
      print(tabulate([["weight",w],["area",area],["xm",xm],["ym",ym],["Ixx",Ixx],["Iyy",Iyy],["rxx",rxx],["ryy",ryy],["Zexx",Zexx],["Zeyy",Zeyy],["xp",xp],["yp",yp],["Zpxx",Zpxx],["Zpyy",Zpyy]]))

   def FMOA(self,x=0,y=0):
      FMOA_x = 0
      FMOA_y = 0
      for shape in self.shapes:
         FMOA_x = FMOA_x + shape.FMOA(0,0)[0]
         FMOA_y = FMOA_y + shape.FMOA(0,0)[1]
      return FMOA_x, FMOA_y

   def centroid(self):
      area = abs(self.area())
      FMOA_x=0
      FMOA_y=0
      for shape in self.shapes:
         FMOA_x = FMOA_x + shape.FMOA(0,0)[0]
         FMOA_y = FMOA_y + shape.FMOA(0,0)[1]
      x_centroid = FMOA_y/area
      y_centroid = FMOA_x/area
      return x_centroid,y_centroid

   def SMOA(self, x, y):
      SMOA_x = 0
      SMOA_y = 0
      for shape in self.shapes:
         SMOA_x = SMOA_x + shape.SMOA(x,y)[0]
         SMOA_y = SMOA_y + shape.SMOA(x,y)[1]
      return SMOA_x, SMOA_y

   def inertia(self):
      Ixx=0
      Iyy=0
      xm,ym=self.centroid()
      for shape in self.shapes:
         Ixx = Ixx + shape.SMOA(xm,ym)[0]
         Iyy = Iyy + shape.SMOA(xm,ym)[1]
      return Ixx, Iyy
   
   def extreme_coordinates(self):
      xl_list=[]
      xu_list=[]
      yl_list=[]
      yu_list=[]
      for shape in self.shapes:
         xl,yl,xu,yu = shape.extreme_coordinates()
         xl_list.append(xl)
         xu_list.append(xu)
         yl_list.append(yl)
         yu_list.append(yu)
      return min(xl_list),min(yl_list),max(xu_list),max(yu_list)
   
   def PNA(self):
      xl,yl,xu,yu = self.extreme_coordinates()
      half_area =self.area()/2
      xp = REGULA_FALSI_METHOD(xl,xu,self.area_below_yy_axis,half_area)
      yp = REGULA_FALSI_METHOD(yl,yu,self.area_below_xx_axis,half_area)
      return xp, yp

   def elastic_section_modulus(self):
      xl,yl,xu,yu = self.extreme_coordinates()
      Ixx,Iyy = self.inertia()
      xm,ym=self.centroid()
      return Ixx/max(abs(yu-ym),abs(yl-ym)), Iyy/max(abs(xu-xm),abs(xl-xm))

   def plastic_section_modulus(self):
      xp, yp = self.PNA()
      Zpbxx= 0
      Zpaxx= 0
      Zpbyy= 0
      Zpayy= 0
  

      for shape in self.shapes_below_xx_axis(yp):
         Zpbxx = Zpbxx + shape.FMOA(xp,yp)[0]
      for shape in self.shapes_above_xx_axis(yp):
         Zpaxx = Zpaxx + shape.FMOA(xp,yp)[0]
      Zpxx = abs(Zpbxx)+abs(Zpaxx)

      for shape in self.shapes_below_yy_axis(xp):
         Zpbyy = Zpbyy + shape.FMOA(xp,yp)[1]
      for shape in self.shapes_above_yy_axis(xp):
         Zpayy = Zpayy + shape.FMOA(xp,yp)[1]
      Zpyy = abs(Zpbyy)+abs(Zpayy)
      return Zpxx, Zpyy

   def shapes_below_xx_axis(self, y):
      shape_list=[]
      for shape in self.shapes:
         line_list=shape.lines_below_xx_axis(y)
         point_list=[]
         shape_list.append(Shape(point_list,line_list))
      return shape_list
   
   def shapes_above_xx_axis(self, y):
      shape_list=[]
      for shape in self.shapes:
         line_list=shape.lines_above_xx_axis(y)
         point_list=[]
         shape_list.append(Shape(point_list,line_list))
      return shape_list

   def shapes_below_yy_axis(self, x):
      shape_list=[]
      for shape in self.shapes:
         line_list=shape.lines_below_yy_axis(x)
         point_list=[]
         shape_list.append(Shape(point_list,line_list))
      return shape_list

   def shapes_above_yy_axis(self, x):
      shape_list=[]
      for shape in self.shapes:
         line_list=shape.lines_above_yy_axis(x)
         point_list=[]
         shape_list.append(Shape(point_list,line_list))
      return shape_list


   def area_below_xx_axis(self, y):
      area = 0
      for shape in self.shapes:
         area = area + shape.area_below_xx_axis(y)
      return area

   def area_above_xx_axis(self, y):
      area = 0
      for shape in self.shapes:
         area = area + shape.area_above_xx_axis(y)
      return area
   
   def area_below_yy_axis(self, x):
      area = 0
      for shape in self.shapes:
         area = area + shape.area_below_yy_axis(x)
      return area
   
   def area_above_yy_axis(self, x):
      area = 0
      for shape in self.shapes:
         area = area + shape.area_above_yy_axis(x)
      return area
   