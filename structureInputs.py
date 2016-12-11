# -*- coding: utf-8 -*-
"""List of constants and repeated strings."""
water_density = float(62.4)
incorrectinput = str("Input is not correct. Try again.")

def getInputs():
    """Function gathers user inputs for the drilled shaft and outputs a dict containing a series
    of drilled shaft foundation, soil, and applied load properties:
    structParams = {'factoredMoment': m_total, 'factoredTorsion': tor_total,
                   'factoredShear': p_total, 'shaftDiameter': shaft_diameter,
                   'sfTor': sf_tor, 'sfOT': sf_ot, 'soilType': soil_type,
                   'soilAOF': soil_aof, 'soilSS': soil_ss, 'offset': shaft_offset}"""
    """Begin asking user for soil and shaft parameter inputs and check each for viablility."""
    while True:
        try:
            soil_type = str(raw_input("What is the soil type (sand/clay)? "))
            if soil_type.lower() == "sand":
                soil_type = soil_type.lower()
                break
            elif soil_type.lower() == "clay":
                soil_type = str(soil_type.lower())
                break
            else:
                print(incorrectinput)
        except ValueError:
            print(incorrectinput)
    while True:
        try:
            nBlows = float(raw_input("Number of blows per foot (<5 contact district geotechnical Engineer)?"))
            if nBlows < 5:
                print "Contact the district geotechnical Engineer for N_blows less than 5"
            break
        except ValueError:
            print(incorrectinput)
    while True:
        water_elevation = raw_input("Is the design water elevation above the top of the foundation or below bottom of the shaft (above/below)? ")
        if water_elevation.lower() == "above" or water_elevation.lower() == "below":
            water_elevation = str(water_elevation)
            break
        else:
            print(incorrectinput)
    while True:
        try:
            soil_density_dry = float(input("What is the saturated soil density (pcf)? ")) #Dry soil density from geotechnical analysis
            if soil_density_dry > 0:
                break
            else:
                print(incorrectinput)
        except ValueError:
            print(incorrectinput)
    while True:
        try:
            shaft_offset = float(input("What is the shaft offset(groundline to top) in ft? "))
            if shaft_offset >= 0:
                shaft_offset = round(shaft_offset, 1)
                break
            else:
                print(incorrectinput)
        except ValueError:
            print(incorrectinput)
    """Calculate soil density"""
    if water_elevation == "above":
        soil_density = float(soil_density_dry) - float(water_density)
    else:
        soil_density = float(soil_density_dry)
    print("The calculated calculated effective soil density is %s pcf" % soil_density)
    while True:
        try:
            shaft_diameter = float(raw_input("What is the shaft diameter (ft)? "))
            if shaft_diameter >= 3.0 and shaft_diameter <= 6.0:
                break
            elif shaft_diameter % 0.5 != 0:
                print("Please round up to next 0.5'.")
            else:
                print(incorrectinput)
        except ValueError:
            print(incorrectinput)
    if soil_type == "sand": # If soil is sand ask for angle of friction
        while True:
            try:
                soil_aof = float(raw_input("What is the soil angle of friction (deg)? "))
                if soil_aof >= 10 and soil_aof <= 90:
                    break
                else:
                    print(incorrectinput)
            except ValueError:
                print(incorrectinput)
    if soil_type == "clay": # If soil is clay ask for soil shear strength
        while True:
            try:
                soil_ss = float(raw_input("What is the soil shear strength (kip/ft^2)? "))
                if soil_ss > 0 and soil_ss < 15:
                    break
                else:
                    print(incorrectinput)
            except ValueError:
                print(incorrectinput)
    while True:
        try:
            sf_ot = float(raw_input("What is saftey factor against overturning (FDOT SM Vol-9 13.6)? "))
            if sf_ot >= 1.0 and sf_ot <= 10.0:
                break
            else:
                print(incorrectinput)
        except ValueError:
            print(incorrectinput)
    while True:
        try:
            sf_tor = float(raw_input("What is the saftey factor against torsion (1.0 for Mast Arms and 1.3 for Overhead Signs)? "))
            if sf_ot >= 1.0 and sf_ot <= 3.0:
                break
            else:
                print(incorrectinput)
        except ValueError:
            print(incorrectinput)
    """Begin asking user for applied load inputs."""
    while True:
        try:
            moment_x = float(raw_input("What is the applied moment about the x-plane (kip-ft)? "))
            if moment_x >= 0.0:
                break
            else:
                print(incorrectinput)
        except ValueError:
            print(incorrectinput)
    while True:
        try:
            shear_x = float(raw_input("What is the applied shear force in the x-plane (kip)? "))
            if shear_x >= 0.0:
                break
            else:
                print(incorrectinput)
        except ValueError:
            print(incorrectinput)
    while True:
        try:
            torsion = float(raw_input("What is the applied torsion (kip-ft)?"))
            if torsion >= 0.0:
                break
            else:
                print(incorrectinput)
        except ValueError:
            print(incorrectinput)
    while True:
        try:
            moment_z = float(raw_input("What is the applied moment about the z-plane (kip-ft)? "))
            if moment_z >= 0.0:
                break
            else:
                print(incorrectinput)
        except ValueError:
            print(incorrectinput)
    while True:
        try:
            shear_z = float(raw_input("What is the applied shear force in the z-plane (kip)? "))
            if shear_z >= 0.0:
                break
            else:
                print(incorrectinput)
        except ValueError:
            print(incorrectinput)
    while True:
        try:
            axial = float(raw_input("What is the applied axial load (kip)? "))
            if axial >= 0.0:
                break
            else:
                print(incorrectinput)
        except ValueError:
            print(incorrectinput)
    m_total = (sf_ot) * ((moment_x ** 2) + (moment_z ** 2)) ** .5
    m_total = round(m_total, 2)
    print ("The factored total overturning moment is %s" % m_total), 'kip-ft'
    p_total = (sf_ot) * ((shear_x ** 2) + (shear_z ** 2)) ** .5
    p_total = round(p_total, 2)
    print ("The factored total overturning shear is %s" % p_total), 'kip'
    tor_total = sf_tor * torsion
    tor_total = round(tor_total, 2)
    print ("The factored torsion is %s" % tor_total), 'kip-ft'
    structParams = {'factoredMoment': m_total, 'factoredTorsion': tor_total,
                   'factoredShear': p_total, 'shaftDiameter': shaft_diameter,
                   'sfTor': sf_tor, 'sfOT': sf_ot, 'soilType': soil_type,
                   'soilDensity': soil_density, 'offset': shaft_offset,
                   'nBlows': nBlows, 'waterLevel': water_elevation }
    if soil_type == "sand":
        structParams['soilAOF'] = soil_aof
    if soil_type == "clay":
        structParams['soilSS'] = soil_ss
    return structParams

if __name__ == "__main__":
    getInputs()
