from tabulate import tabulate
from math import pi, cos,sin, sqrt,tan
from class_geometry import Geometry, Point, Line, C_curve, Shape
class C_section(Geometry):
    def __init__(self, h,b,tf,tw,D,r1,r2):
        self.name = "Channel section"
        self.h = h
        self.b = b
        self.tf = tf
        self.tw = tw
        self.D = D
        self.r1 = r1
        self.r2 = r2
        super().__init__([self.shape()])
        # self.area = self.section.area()
        
    def __str__(self):
        table1 = [["-",f"{self.name}"],["h",self.h],["b",self.b],["tf",self.tf],["tw",self.tw],["D",self.D],["r1",self.r1],["r2",self.r2]]
        
        area =self.area()
        xm,ym = self.centroid()
        Ixx, Iyy = self.inertia()
        rxx,ryy = sqrt(Ixx/area), sqrt(Iyy/area)
        Zexx, Zeyy = self.elastic_section_modulus() 
        xp, yp = self.PNA() 
        Zpxx, Zpyy = self.plastic_section_modulus() 
        table2=[["","properties"],["a",area],["Cxx",ym],["Cyy",xm],["Ixx",Ixx],["Iyy",Iyy],["rxx",rxx],["ryy",ryy],["Zexx",Zexx],["Zeyy",Zeyy],["Cpxx",yp],["Cpyy",xp],["Zpxx",Zpxx],["Zpyy",Zpyy]]
        
        return tabulate([[tabulate(table1,tablefmt="simple_grid"),tabulate(table2,tablefmt="simple_grid")]],tablefmt="plain")
    
    def properties(self):
        area =self.area()
        w = area*7850/(1000**2)
        xm,ym = self.centroid()
        Ixx, Iyy = self.inertia()
        rxx,ryy = sqrt(Ixx/area), sqrt(Iyy/area)
        Zexx, Zeyy = self.elastic_section_modulus() 
        xp, yp = self.PNA() 
        Zpxx, Zpyy = self.plastic_section_modulus() 
        return w, area, xm,ym,Ixx,Iyy,rxx,ryy,Zexx,Zeyy,xp,yp,Zpxx,Zpyy


    def shape(self):
        h=self.h
        b=self.b
        tf=self.tf
        tw=self.tw
        D=self.D 
        r1=self.r1
        r2=self.r2

        Dr=D*pi/180 # Dr is angle in radian
        alpha = Dr-pi/2 
        beta = pi-Dr
        b1=r2-r2*cos(beta)
        b2=(b-tw)/2-b1
        b5=tw
        b4=r1-r1*cos(beta)
        b3=(b-tw)/2-b4
        # b1+b2+b3+b4+b5
        h1=tf-r2*tan(beta/2)-(b-tw)/2*tan(alpha)
        h2=r2*sin(beta)
        h3=(b3+b2)*tan(alpha)
        h4=r1*sin(beta)
        p1=Point(0,0)
        p2=Point(b,0)
        p3=Point(b,h1)
        p4=Point(b-b1,h1+h2)
        p5=Point(b5+b4,h1+h2+h3)
        p6=Point(tw,h1+h2+h3+h4)
        p7=Point(tw,h-(h1+h2+h3+h4))
        p8=Point(b5+b4,h-(h1+h2+h3))
        p9=Point(b-b1,h-(h1+h2))
        p10=Point(b,h-h1)
        p11=Point(b,h)
        p12=Point(0,h)

        pc1=Point(b-r2,h1,type="centre")
        pc2=Point(tw+r1,h1+h2+h3+h4,type="centre")
        pc3=Point(tw+r1,h-(h1+h2+h3+h4),type="centre")
        pc4=Point(b-r2,h-h1,type="centre")

        l1=Line(p1,p2)
        l2=Line(p2,p3)
        c3=C_curve(p3,p4,pc1)
        l4=Line(p4,p5)
        c5=C_curve(p5,p6,pc2)
        l6=Line(p6,p7)
        c7=C_curve(p7,p8,pc3)
        l8=Line(p8,p9)
        c9=C_curve(p9,p10,pc4)
        l10=Line(p10,p11)
        l11=Line(p11,p12)
        l12=Line(p12,p1)

        point_list=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12]
        line_list=[l1,l2,c3,l4,c5,l6,c7,l8,c9,l10,l11,l12]
        
        return Shape(point_list,line_list)

class I_section(Geometry):
    def __init__(self, h,b,tf,tw,D,r1,r2):
        self.name = "I section"
        self.h = h
        self.b = b
        self.tf = tf
        self.tw = tw
        self.D = D
        self.r1 = r1
        self.r2 = r2
        super().__init__([self.shape()])
    
    def properties(self):
        area =self.area()
        w = area*7850/(1000**2)
        xm,ym = self.centroid()
        Ixx, Iyy = self.inertia()
        rxx,ryy = sqrt(Ixx/area), sqrt(Iyy/area)
        Zexx, Zeyy = self.elastic_section_modulus() 
        xp, yp = self.PNA() 
        Zpxx, Zpyy = self.plastic_section_modulus() 
        return w, area, xm,ym,Ixx,Iyy,rxx,ryy,Zexx,Zeyy,xp,yp,Zpxx,Zpyy

    def __str__(self):
        table1 = [["-",f"{self.name}"],["h",self.h],["b",self.b],["tf",self.tf],["tw",self.tw],["D",self.D],["r1",self.r1],["r2",self.r2]]
        
        area =self.area()
        xm,ym = self.centroid()
        Ixx, Iyy = self.inertia()
        rxx,ryy = sqrt(Ixx/area), sqrt(Iyy/area)
        Zexx, Zeyy = self.elastic_section_modulus() 
        xp, yp = self.PNA() 
        Zpxx, Zpyy = self.plastic_section_modulus() 
        table2=[["","properties"],["a",area],["Cxx",ym],["Cyy",xm],["Ixx",Ixx],["Iyy",Iyy],["rxx",rxx],["ryy",ryy],["Zexx",Zexx],["Zeyy",Zeyy],["Cpxx",yp],["Cpyy",xp],["Zpxx",Zpxx],["Zpyy",Zpyy]]
        
        return tabulate([[tabulate(table1,tablefmt="simple_grid"),tabulate(table2,tablefmt="simple_grid")]],tablefmt="plain")


    def shape(self):
        h=self.h
        b=self.b
        tf=self.tf
        tw=self.tw
        D=self.D 
        r1=self.r1
        r2=self.r2

        Dr=D*pi/180 # Dr is angle in radian
        alpha = Dr-pi/2 
        beta = pi-Dr
        b1=r2-r2*cos(beta)
        b2=(b-tw)/4-b1

        b4=r1-r1*cos(beta)
        b3=(b-tw)/4-b4
        # b1+b2+b3+b4+b5
        h1=tf-r2*tan(beta/2)-(b-tw)/4*tan(alpha)
        h2=r2*sin(beta)
        h3=(b3+b2)*tan(alpha)
        h4=r1*sin(beta)

        p1=Point(0,0)
        p2=Point(b,0)
        p3=Point(b,h1)
        p4=Point(b-b1,h1+h2)
        p5=Point(b-(b1+b2+b3),h1+h2+h3)
        p6=Point(b-(b1+b2+b3+b4),h1+h2+h3+h4)
        p7=Point(b-(b1+b2+b3+b4),h-(h1+h2+h3+h4))
        p8=Point(b-(b1+b2+b3),h-(h1+h2+h3))
        p9=Point(b-b1,h-(h1+h2))
        p10=Point(b,h-h1)
        p11=Point(b,h)
        p12=Point(0,h)
        p13=Point(0,h-h1)
        p14=Point(b1,h-(h1+h2))
        p15=Point(b1+b2+b3, h-(h1+h2+h3))
        p16=Point(b1+b2+b3+b4, h-(h1+h2+h3+h4))
        p17=Point(b1+b2+b3+b4,h1+h2+h3+h4)
        p18=Point(b1+b2+b3,h1+h2+h3)
        p19=Point(b1,h1+h2)
        p20=Point(0,h1)

        pc1=Point(r2,h1,type="centre")
        pc2=Point(b-r2,h1,type="centre")
        pc3=Point(b1+b2+b3+b4+tw+r1,h1+h2+h3+h4,type="centre")
        pc4=Point(b1+b2+b3+b4+tw+r1,h-(h1+h2+h3+h4),type="centre")
        pc5=Point(b-r2,h-h1,type="centre")
        pc6=Point(r2,h-h1,type="centre")
        pc7=Point(b1+b2+b3+b4-r1,h-(h1+h2+h3+h4),type="centre")
        pc8=Point(b1+b2+b3+b4-r1,h1+h2+h3+h4,type="centre")

        l1=Line(p1,p2)
        l2=Line(p2,p3)
        c3=C_curve(p3,p4,pc2)
        l4=Line(p4,p5)
        c5=C_curve(p5,p6,pc3)
        l6=Line(p6,p7)
        c7=C_curve(p7,p8,pc4)
        l8=Line(p8,p9)
        c9=C_curve(p9,p10,pc5)
        l10=Line(p10,p11)
        l11=Line(p11,p12)
        l12=Line(p12,p13)
        c13=C_curve(p13,p14,pc6)
        l14=Line(p14,p15)
        c15=C_curve(p15,p16,pc7)
        l16=Line(p16,p17)
        c17=C_curve(p17,p18,pc8)
        l18=Line(p18,p19)
        c19=C_curve(p19,p20,pc1)
        l20=Line(p20,p1)

        if r1 >0 and r2 >0 :
            point_list=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20]
            line_list=[l1,l2,c3,l4,c5,l6,c7,l8,c9,l10,l11,l12,c13,l14,c15,l16,c17,l18,c19,l20]
        elif r1>0 and r2==0:
            point_list=[p1,p2,p3,p5,p6,p7,p8,p10,p11,p12,p13,p15,p16,p17,p18,p20]
            line_list=[l1,l2,l4,c5,l6,c7,l8,l10,l11,l12,l14,c15,l16,c17,l18,l20]
        elif r1==0 and r2>0:
            point_list=[p1,p2,p3,p4,p5,p8,p9,p10,p11,p12,p13,p14,p15,p18,p19,p20]
            line_list=[l1,l2,c3,l4,l6,l8,c9,l10,l11,l12,c13,l14,l16,l18,c19,l20]
        elif r1==0 and r2==0:
            point_list=[p1,p2,p3,p5,p8,p10,p11,p12,p13,p15,p18,p20]
            line_list=[l1,l2,l4,l6,l8,l10,l11,l12,l14,l16,l18,l20]
        return Shape(point_list,line_list)

