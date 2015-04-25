from ephemerides import *
from quaternion import *
from rosettaConfiguration import *

class AutonomousGuidance: 

    def __init__(self, e):
        self._ephemerides = e 
        self._pointedAxis = Vector(1, 0, 0)
        self._earthPointing = True
        self._ecliptic = True
        self._yNorth = True

        config = RosettaConfiguration()

        if config.getItem('AUTO_EARTH_POINTING') == 'TRUE':
            self.setEarthPointing()
        else:
            self.setSunPointing()
        if config.getItem('AUTO_NORTH_POINTING') == 'TRUE':
            self.setNorthPointing()
        else:
            self.setSouthPointing()
        if config.getItem('AUTO_PERP_ECLIPTIC') == 'TRUE':
            self.setPerpendicularToEcliptic()
        else:
            self.setPerpendicularToSunSpacecraft()

        self.setPointedAxis(Vector(float(config.getItem('AUTO_POINTED_X_AXIS')), float(config.getItem('AUTO_POINTED_Y_AXIS')), float(config.getItem('AUTO_POINTED_Z_AXIS'))))


    def setEphemerides(self, e):
        self._ephemerides = e 

    def setEarthPointing(self):
        self._earthPointing = True

    def setSunPointing(self):
        self._earthPointing = False

    def setNorthPointing(self):
        self._yNorth = True

    def setSouthPointing(self):
        self._yNorth = False

    def setPerpendicularToEcliptic(self):
        self._ecliptic = True

    def setPerpendicularToSunSpacecraft(self):
        self._ecliptic = False

    def setPointedAxis(self, a):
        self._pointedAxis = a.norm()
        
    def quaternion(self, t):

        qt = calendar.timegm(t.utctimetuple()) 

        ecliptic_normal = Vector(0.0,-0.3987,0.9171)
        v_sc_axis = Vector(1,0,0)
        v_y_axis = Vector(0,0,0)
    
        if self._earthPointing:
            v_sc_axis = self._ephemerides.earthScVector(qt).normalize().negate()
        else:
            v_sc_axis = self._ephemerides.sunScVector(qt).normalize().negate()

        if self._ecliptic:
            v_y_axis = v_sc_axis.vectorproduct(ecliptic_normal).vectorproduct(v_sc_axis)     
        else:
            v_y_axis = self._ephemerides.earthScVector(qt).vectorproduct(self._ephemerides.sunScVector(qt))

        # compute opposite vector if a pointing to the south ecliptic is required
        if not self._yNorth:
            v_y_axis = v_y_axis.negate()

        v_y_axis.normalize()

        # correct vector in order to compensate for the misalignment of required direction
        #          2
        # Ysc = (1-y/2).Ysc + y.Usc

        v_y_axis =  v_y_axis * (1 - (self._pointedAxis.Y() * self._pointedAxis.Y())/2)  + v_sc_axis * self._pointedAxis.Y()


        v_y_axis.normalize() 

        # compute the spacecraft X axis
        # Xsc = x.Usc - z.(Usc x Ysc) - x.y.Ysc

        v_x_axis = v_sc_axis * self._pointedAxis.X()  - (v_sc_axis.vectorproduct(v_y_axis) * self._pointedAxis.Z()) - (v_y_axis * self._pointedAxis.X() * self._pointedAxis.Y())

        v_x_axis.normalize() 

        # the spacecraft axis completes the direct triad
        # Zsc = Xsc x Ysc

        v_z_axis = v_x_axis.vectorproduct(v_y_axis)

        return Quaternion.createFromVectors(v_x_axis, v_y_axis, v_z_axis)

