import math

def getAirDensity(tempf, rh, baropresin, elevft):
	temp = (tempf - 32.0)*(5.0/9.0)   # convert temperature to degrees Celsius 
	baropres = 25.4*baropresin   # convert barometric presure to mm of mercury 
	elev = 0.3048*elevft     # convert elevation to meters 
	g = 9.80665       # earth's gravitational acceleration 
	M = 0.0289644     # molecular mass of air 
	R = 8.31447       # universal gas constant 
	airpres = baropres*math.exp( (-g*M*elev) / (R*(temp+273.15)))  # absolute atmospheric air pressure 
	svp = 4.5841*math.exp( ((18.687 - temp/234.5)*temp)/(257.14+temp))   # Buck approximation to saturation vapor pressure 
	airdensity = 1.2929*(273.0/(temp+273.0))*((airpres - svp*rh/100.0)/760.0)  # air density in kg/m^3 
	
	return airdensity;


print(getAirDensity(75, 49, 30.04, 10))
print(getAirDensity(88, 34, 29.98, 5190))
print(getAirDensity(94, 63, 29.97, 45))
print(getAirDensity(83, 59, 29.96, 815))
print(getAirDensity(104, 20, 29.81, 1086))
print(getAirDensity(68, 65, 29.99, 0))
