# -*- coding:Utf8 -*-

"How to run a simulation using Python and Dymola."

from buildingspy.simulate.Simulator import Simulator

# Test 1
# model = 'SolarSystem.Testing.Mixing_air_flow'
# s = Simulator(model, 'dymola', "test")
# s.addParameters({"Fan.vol.tau": 22,                  # Can change second level and protected value.
#                  "vol.V": 44,                        # Can change first level value.
#                  "TT.n": 3,
#                  "TT.wait_for": [100, 200]})  # Can pass array to constructor (do not use subscripts)
# datConExtWin(each layers=Wall, each A=26.4, each glaSys=GlaSys_Argon, wWin={1.36 + 1.35,0.6,0.9 + 1.6,2.4 + 1.2}, hWin={1.2 + 1.2,0.95,2.15 + 2.15,2.15 + 1.35}, each fFra=0.1, each til=W_, azi={NW_,NE_,SW_,SE_})

# Test 2
model = "SolarSystem.Models.Systems.IGC_system.House.IGC_house_Simulation"
s = Simulator(model, 'dymola', "test")
# Access a record parameter (for instance a data structure in the house model of a wall)
s.addParameters({"House.datConExtWin.wWin": [1.36 + 1.35, 0.6, 0.9 + 1.6, 2.4 + 1.2],
                 "House.datConExtWin.A": [30, 30, 30, 30]})

s.setStopTime(1000)
s.setTimeOut(40)
s.printModelAndTime()
s.showProgressBar(False)
s.showGUI(True)
s.exitSimulator(exitAfterSimulation=False)
s.simulate()
