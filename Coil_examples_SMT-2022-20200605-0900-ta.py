this_program= "Coil_examples_SMT-2020-20200605-0900-ta.py"
print( "This is '",this_program,"'...")
# =========================================================
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# INPUT:	none
# OUTPUT:	none
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# Tabea Arndt
#
# KIT
# ITEP
#
# =========================================================
#libs####################################################################
import math                                     						#needed for exponentials
import os                                       						#needed to start external programs
#import subprocess                               						#might be needed to start external programs
import numpy as np                              						#needed for array-operations
from numpy import linalg as LA											#for use of LA.norm()
import matplotlib.pyplot as plt                 						#plotting library
import matplotlib.cm as cm												#for colormap
from mpl_toolkits import mplot3d										#
opsys= "WINDOWS"														#zur späteren Selektion von Spezifika wird das Betriebssystem angegeben
#opsys= "OTHER"															#
if opsys == "WINDOWS": import msvcrt as ms								#works for ms-windows only (get better access to terminal, especially keypress); if no equivalent "keypress" has to be substituted (see below)
#functions###############################################################
def parameters_menue():													#-p-#change parameters
	global selected_trajectories, no_sections_traj, I_traj, ix_max, x_min, x_max, iz_max, z_min, z_max
	direction_values_changed= False
	while True:
		my_cls()
		print( "PARAMETER MENUE")
		print( "==========================================================")
		print( "0=return to main menue")
		print( "1=selected trajectories (no sep. by ,)  : ", selected_trajectories)
		print( "2=number of sections of trajectory      : ", no_sections_traj)
		print( "3=current on trajectory              [A]: ", I_traj)
		print( "4=number of grid points per direction 	: ", ix_max)
		print( "5=minimum value of physical x        [m]: ", x_min)
		print( "6=maximum value of physical x        [m]: ", x_max)
		print( "7=minimum value of physical z        [m]: ", z_min)
		print( "8=maximum value of physical z        [m]: ", z_max)
		print( "Auto-settings............................")
		print( "a=setting for single current loop")
		print( "s=setting for solenoid")
		print( "f=setting for solenoid for vector-plot")
		print( "h-setting for Helmholtz-configuration")
		print( "m-setting for Maxwell-/Braunbek-configuration")
		print( "b-setting for Barker-configuration")
		print( "d-setting for circular dipole")
		print( "q-setting for circulare quadrupole")
		key= my_keypress()
		if key =='0':
			if direction_values_changed: adjust_global_vars()
			my_cls()
			print( "Remember to re-calculate in MAIN MENUE!!! - Any key to contine...")
			key= my_keypress()
			return()
		elif key=='1': selected_trajectories= input(); direction_values_changed= True
		elif key=='2': no_sections_traj= eval( input()); direction_values_changed= True
		elif key=='3': I_traj=		eval( input())
		elif key=='4': ix_max= 		eval( input()); iz_max= ix_max; direction_values_changed= True
		elif key=='5': x_min= 		eval( input()); direction_values_changed= True
		elif key=='6': x_max= 		eval( input()); direction_values_changed= True
		elif key=='7': z_min= 		eval( input()); direction_values_changed= True
		elif key=='8': z_max= 		eval( input()); direction_values_changed= True
		elif key=='a': 													#setting for single current loop
			selected_trajectories= "0";
			x_min= -math.pi/10; x_max= -x_min; z_min= -0.3; z_max= 0.9;
			direction_values_changed= True;
			print("Setting for single current loop done!\a", flush= True) #report and chime
		elif key=='s':													#setting for solenoid
			selected_trajectories= "8"
			I_traj= 1E3; ix_max= 40; iz_max= ix_max; no_sections_traj= 3600
			x_min= -math.pi/10; x_max= -x_min; z_min= -0.3; z_max= 0.5
			direction_values_changed= True;
			print("Setting for solenoid done!\a", flush= True)			#report and chime
		elif key=='f':													#setting for solenoid for vector plot
			selected_trajectories= "8"
			I_traj= 1E4; ix_max= 41; iz_max= ix_max; no_sections_traj= 3600
			x_min= -0.041; x_max= -x_min; z_min= -0.151; z_max= 0.451
			direction_values_changed= True
			print("Setting for solenoid for vector-plot done!\a", flush= True)			#report and chime
		elif key=='h':
			selected_trajectories= "0,1"
			I_traj= 2E5; ix_max= 20; iz_max= ix_max; no_sections_traj= 90
			x_min= -0.1-math.pi/10; x_max= -x_min; z_min= -0.1-math.pi/10; z_max= -z_min;
			direction_values_changed= True;
			print("Setting for Helmholtz-configuration done!\a", flush= True)			#report and chime
		elif key=='m':
			selected_trajectories= "0,1,4,5"
			I_traj= 2E5; ix_max= 20; iz_max= ix_max; no_sections_traj= 90
			x_min= -0.1-math.pi/10; x_max= -x_min; z_min= -0.1-math.pi/10; z_max= -z_min;
			direction_values_changed= True;
			print("Setting for Helmholtz-/Braunbek-configuration done!\a", flush= True)			#report and chime
		elif key=='b':
			selected_trajectories= "0,1,6,7,10,11"
			I_traj= 1E5; ix_max= 20; iz_max= ix_max; no_sections_traj= 90
			x_min= -0.1-math.pi/10; x_max= -x_min; z_min= -0.1-math.pi/10; z_max= -z_min;
			direction_values_changed= True;
			print("Setting for Barker-configuration done!\a", flush= True)			#report and chime
		elif key=='d':
			selected_trajectories= "21,22"
			I_traj= 1E5; ix_max= 20; iz_max= ix_max; no_sections_traj= 90
			x_min= -0.1-math.pi/10/10; x_max= -x_min; z_min= -0.1-math.pi/10/10; z_max= -z_min;
			direction_values_changed= True;
			print("Setting for circular dipol done!\a", flush= True)	#report and chime
		elif key=='q':
			selected_trajectories= "31,32"
			I_traj= 1E4; ix_max= 40; iz_max= ix_max; no_sections_traj= 180
			x_min= -0.1-math.pi/40; x_max= -x_min; z_min= -0.1-math.pi/40; z_max= -z_min;
			direction_values_changed= True;
			print("Setting for circular quadrupole done!\a", flush= True)	#report and chime
	return()
def Trajectory_point( t, t_max, trajectory_index):						#compute point on trajectory of current according to parameter and index of trajectory
	x=0; y=1; z=2														#for convenience
	T= np.array( [+0.,+0.,+0.])											#init result
	#define parametrized trajectory according to trajectory index...
	if trajectory_index == 0:											#Trajectory #0: circular loop in physical xy-plane at z=+R
		R= 0.300														#radius
		alpha= 2*math.pi*t/t_max										#angle
		T[x]= R * math.cos( alpha)										#x-coordinate
		T[y]= R * math.sin( alpha)										#y-coordinate
		T[z]= +R 	            										#z-coordinate
	elif trajectory_index == 1:											#Trajectory #1: circular loop in physical xy-plane at z=-R
		R= 0.300														#radius
		alpha= 2*math.pi*t/t_max										#angle
		T[x]= R * math.cos( alpha)										#x-coordinate
		T[y]= R * math.sin( alpha)										#y-coordinate
		T[z]= -R 														#z-coordinate
	elif trajectory_index == 2:											#Trajectory #2: circular loop in physical xy-plane at z=+R/2
		R= 0.300														#radius
		alpha= 2*math.pi*t/t_max										#angle
		T[x]= R * math.cos( alpha)										#x-coordinate
		T[y]= R * math.sin( alpha)										#y-coordinate
		T[z]= +R/2. 													#z-coordinate
	elif trajectory_index == 3:											#Trajectory #3: circular loop in physical xy-plane at z=-R/2
		R= 0.300														#radius
		alpha= 2*math.pi*t/t_max										#angle
		T[x]= R * math.cos( alpha)										#x-coordinate
		T[y]= R * math.sin( alpha)										#y-coordinate
		T[z]= -R/2.														#z-coordinate
	elif trajectory_index == 4:											#Trajectory #4: circular loop in physical xy-plane at z=-R/10
		R= 0.330														#radius
		alpha= 2*math.pi*t/t_max										#angle
		T[x]= R * math.cos( alpha)										#x-coordinate
		T[y]= R * math.sin( alpha)										#y-coordinate
		T[z]= -R/10.													#z-coordinate
	elif trajectory_index == 5:											#Trajectory #5: circular loop in physical xy-plane at z=+R/10
		R= 0.330														#radius
		alpha= 2*math.pi*t/t_max										#angle
		T[x]= R * math.cos( alpha)										#x-coordinate
		T[y]= R * math.sin( alpha)										#y-coordinate
		T[z]= +R/10.													#z-coordinate
	elif trajectory_index == 6:											#Trajectory #6:
		R= 0.300														#radius
		alpha= 2*math.pi*t/t_max										#angle
		T[x]= R * math.cos( alpha)										#x-coordinate
		T[y]= R * math.sin( alpha)										#y-coordinate
		T[z]= +R/10.													#z-coordinate
	elif trajectory_index == 7:											#Trajectory #7:
		R= 0.300														#radius
		alpha= 2*math.pi*t/t_max										#angle
		T[x]= R * math.cos( alpha)										#x-coordinate
		T[y]= R * math.sin( alpha)										#y-coordinate
		T[z]= -R/10.													#z-coordinate
	elif trajectory_index == 8:											#Trajectory #8: solenoid (helix) z=0...L; REMEMBER TO SET TRAJECTORY SCANS TO >3600, z_max=0.5!
		L= 0.300
		R= L/10.
		alpha= 2*math.pi*t/36											#angle
		T[x]= R * math.cos( alpha)										#x-coordinate
		T[y]= R * math.sin( alpha)										#y-coordinate
		T[z]= 0.01 * L * int(t/36)										#z-coordinate
	elif trajectory_index == 10:										#Trajectory #9: circular current loop in physical xy-plane at z= +R*1.1
		R= 0.300														#radius
		alpha= 2*math.pi*t/t_max										#angle
		T[x]= R * math.cos( alpha)										#x-coordinate
		T[y]= R * math.sin( alpha)										#y-coordinate
		T[z]= R * 1.1													#z-coordinate
	elif trajectory_index == 11:										#Trajectory #9: circular current loop in physical xy-plane at z= -R*1.1
		R= 0.300														#radius
		alpha= 2*math.pi*t/t_max										#angle
		T[x]= R * math.cos( alpha)										#x-coordinate
		T[y]= R * math.sin( alpha)										#y-coordinate
		T[z]= -R * 1.1													#z-coordinate
	if trajectory_index == 21:											#Trajectory #0: circular loop in physical xy-plane at z=+R
		R= 0.050														#radius
		alpha= 2*math.pi*t/t_max										#angle
		T[x]= R * math.cos( alpha)										#x-coordinate
		T[y]= R * math.sin( alpha)										#y-coordinate
		T[z]= +R/10.            										#z-coordinate
	if trajectory_index == 22:											#Trajectory #0: circular loop in physical xy-plane at z=+R
		R= 0.050														#radius
		alpha= 2*math.pi*t/t_max										#angle
		T[x]= R * math.cos( alpha)										#x-coordinate
		T[y]= R * math.sin( alpha)										#y-coordinate
		T[z]= -R/10.            										#z-coordinate
	if trajectory_index == 31:											#Trajectory #0:::::::::::::::::::::::::::::::::::::::::::::::
		R= 0.050														#radius
		alpha= +2*math.pi*t/t_max										#angle
		T[x]= R * math.cos( alpha)										#x-coordinate
		T[y]= R * math.sin( alpha)										#y-coordinate
		T[z]= +R*1.00            										#z-coordinate
	if trajectory_index == 32:											#Trajectory #0::::::::::::::::::::::::::::::::::::::::::::::::
		R= 0.050														#radius
		alpha= -2*math.pi*t/t_max										#angle
		T[x]= R * math.cos( alpha)										#x-coordinate
		T[y]= R * math.sin( alpha)										#y-coordinate
		T[z]= -R*1.00            										#z-coordinate
	if trajectory_index == 33:											#Trajectory #0:::::::::::::::::::::::::::::::::::::::::::::::
		R= 0.050														#radius
		alpha= -2*math.pi*t/t_max										#angle
		T[x]= R * math.cos( alpha)										#x-coordinate
		T[y]= R * math.sin( alpha)										#y-coordinate
		T[z]= +R*1.00            										#z-coordinate
	if trajectory_index == 34:											#Trajectory #0:::::::::::::::::::::::::::::::::::::::::::::::
		R= 0.050														#radius
		alpha= -2*math.pi*t/t_max										#angle
		T[x]= R * math.cos( alpha)										#x-coordinate
		T[y]= R * math.sin( alpha)										#y-coordinate
		T[z]= -R*1.00           										#z-coordinate
	return( T)															#return result vector
def Bstar_by_line( T0, T1, P):											#vector of magnetic field per unit current by line(T0,T1) at point P
	R0=T0-P																#create differential vectors for section points to observer
	R1=T1-P																#create differential vectors for section points to observer
	Bstar= np.array( [ 0., 0., 0.])										#init vector
	r0=LA.norm( R0)														#for convenience
	r1=LA.norm( R1)														#for convenience
	Bstar= np.cross( R0, R1)/r0/r1*(r0+r1)/(r0*r1+np.dot(R0, R1))*1E-7  #Wilson p.39 (3.39)
	return( Bstar)														#return vector of magnetic field
def B_by_complete_trajectory( P, trajectory_index):						#compute and return complete B-vector at P over all sections of the given trajectory and according current
	global no_sections_traj, I_traj										#use global vars
	B=	np.array( [0., 0., 0.])											#init vektor
	for i in range( 0, no_sections_traj):								#scan line segments of trajectory of current
		P0= Trajectory_point( i, no_sections_traj, trajectory_index)	#get starting point of line segment of trajectory
		P1= Trajectory_point( i+1, no_sections_traj, trajectory_index)	#get ending point
		B+= Bstar_by_line( P0, P1, P)									#add contribution
		#print( ".", end="", flush= True)								#indicate progress
	B*= I_traj															#multiply by current
	return( B)															#return B-vector
def plot_B_vector():													#XXX
	print( "Plot_B_vector in xz-plane...")								#report
	plt.title( "(Bx,Bz)-vector in xz-plane")
	plt.xlabel( "x")													#set xlabel
	plt.ylabel( "z")													#set ylabel
	plt.quiver( XP, YP, ZZP[0,:], ZZP[2,:])								#create plot
	plt.show()															#show plot
	plt.clf()															#clear plot
	print( "...done")													#report
	return()															#
def plot_Bz_vs_z():														#-1-#plot Bz(<x>,y=0,z) on y-vs-x-plot
	global xp, yp, iz_max, ZZP											#global vars
	print( "Displaying Bz(<x>,y=0,z)...")								#report
	x_pvals= [ 0]														#init plot values...
	y1_pvals= [ 0]														#...
	y2_pvals= [ 0]														#
	y3_pvals= [ 0]
	x_pvals.clear()														#clear plot values...
	y1_pvals.clear()													#...
	y2_pvals.clear()													#
	y3_pvals.clear()
	for ipx in range( 0, iz_max):										#scan physical z-axis (on x-plot)
		x_pvals.append(	YP[ ipx, int( len( xp)/2)] )					#append meshpoint YP(i,<x>) to the x-plot-axis (YP is scanned on first index)
		y1_pvals.append( ZZP[ 0, ipx, int( len( xp)/2)] )				#append Bx(<x>,y=0,z by ipx) to y1-plot
		y2_pvals.append( ZZP[ 1, ipx, int( len( xp)/2)] )				#append Bx(<x>,y=0,z by ipx) to y1-plot
		y3_pvals.append( ZZP[ 2, ipx, int( len( xp)/2)] )				#append Bx(<x>,y=0,z by ipx) to y1-plot
	plt.xlabel( 'z [m]')												#set x-plot-label
	plt.ylabel( 'B [T]')												#set y-plot-label
	plt.title( "Bz(<x>,y=0,z)")											#set title
	plt.plot( x_pvals, y3_pvals, label='Bz')							#plot
	plt.legend( loc='upper left')										#position legend
	plt.show()															#show plot
	plt.clf()															#clear plot
	print( "...done")													#report
	return()															#return
def plot_B_vs_x():														#-2-#plot Bx,y,z(x,y=0,<z>)
	global xp, yp, ix_max, XP, ZZP										#global vars
	print( "Displaying Bx,y,z(x,y=0,<z>)...")							#report
	x_pvals= [ 0]														#init plot values...
	y1_pvals= [ 0]														#
	y2_pvals= [ 0]														#
	y3_pvals= [ 0]
	x_pvals.clear()														#clear plot values...
	y1_pvals.clear()													#
	y2_pvals.clear()													#
	y3_pvals.clear()
	for ix in range( 0, ix_max):										#scan all physical (x,y=0,<z>)
		x_pvals.append(		XP[ int( len( yp)/2), ix])					#append meshpoint of XP(<z>,i) to the x-plot (XP is scanned on second index)
		y1_pvals.append( 	ZZP[ 0, int( len( yp)/2), ix] )				#append Bx(ix,y=0,<z>) to y1-plot
		y2_pvals.append( 	ZZP[ 1, int( len( yp)/2), ix] )				#append By(ix,y=0,<z>) to y2-plot
		y3_pvals.append( 	ZZP[ 2, int( len( yp)/2), ix] )				#append Bz(ix,y=0,<z>) to y3-plot
	plt.xlabel( 'x [m]')												#set x-plot-label
	plt.ylabel( 'B [T]')												#set y-plot-label
	plt.title( "Bx,y,z(x,y=0,<z>)")										#set title
	plt.plot( x_pvals, y1_pvals, label='Bx')							#plot first data
	plt.plot( x_pvals, y2_pvals, label='By')							#plot second data
	plt.plot( x_pvals, y3_pvals, label='Bz')							#plot second data
	plt.legend( loc='upper left')										#position legend
	plt.show()															#show plot
	plt.clf()															#clear plot
	print( "...done")													#report
	return()															#done
def plot_B_vs_z():														#-3-#plot Bx,y,z(<x>,y=0,z) on y-vs-x-plot
	global xp, yp, iz_max, ZZP											#global vars
	print( "Displaying Bx,y,z(<x>,y=0,z)...")							#report
	x_pvals= [ 0]														#init plot values...
	y1_pvals= [ 0]														#...
	y2_pvals= [ 0]														#
	y3_pvals= [ 0]
	x_pvals.clear()														#clear plot values...
	y1_pvals.clear()													#...
	y2_pvals.clear()													#
	y3_pvals.clear()
	for ipx in range( 0, iz_max):										#scan physical z-axis (on x-plot)
		x_pvals.append(	YP[ ipx, int( len( xp)/2)] )					#append meshpoint YP(i,<x>) to the x-plot-axis (YP is scanned on first index)
		y1_pvals.append( ZZP[ 0, ipx, int( len( xp)/2)] )				#append Bx(<x>,y=0,z by ipx) to y1-plot
		y2_pvals.append( ZZP[ 1, ipx, int( len( xp)/2)] )				#append Bx(<x>,y=0,z by ipx) to y1-plot
		y3_pvals.append( ZZP[ 2, ipx, int( len( xp)/2)] )				#append Bx(<x>,y=0,z by ipx) to y1-plot
	plt.xlabel( 'z [m]')												#set x-plot-label
	plt.ylabel( 'B [T]')												#set y-plot-label
	plt.title( "Bx,y,z(<x>,y=0,z)")										#set title
	plt.plot( x_pvals, y1_pvals, label='Bx')							#plot
	plt.plot( x_pvals, y2_pvals, label='By')							#plot
	plt.plot( x_pvals, y3_pvals, label='Bz')							#plot
	plt.legend( loc='upper left')										#position legend
	plt.show()															#show plot
	plt.clf()															#clear plot
	print( "...done")													#report
	return()															#return
def plot_B_contour_and_fill_by_image():									#-4-#plot contour of |B|(x,z) on xy-plot
	print( "B contour and plot by image...")							#report
	for ipx in range( 0, len(xp)):										#scan all elements of xp
		for ipy in range( 0, len(yp)):									#scan all elements of yp
			ZP[ipx, ipy]= LA.norm( ZZP[:, ipx, ipy]) 		   			#let Bz [µT] be the value of ZP-axis
	print( "Displaying contour-line plot...(press mouse to set label and to ESC continue)")
	fig, ax = plt.subplots()											#define figures
	CS = ax.contour(XP, YP, ZP, 15)										#define contour plot
	plt.title('|B|(x,y=0,z) [T]')										#set title
	#manual_locations= [ (2., 0.), (3.,0.)]								#place values at e.g. (2,0) and (3,0)
#	ax.clabel(CS, inline=1, fontsize=10, manual= manual_locations)		#use manual positions of contour labels
#																		#manual without args allows placement by mouse
	ax.clabel(CS, inline=1, fontsize=10, manual= True)					#use manual positions of contour labels
	print( "Displaying filled contour plot...")
	fig, ax = plt.subplots()											#define figures
	im= ax.imshow( ZP, interpolation='bilinear', origin='lower', cmap='RdGy', extent=( xp[0], xp[ix_max-1], yp[0], yp[iz_max-1]))	#'flag' cm.viridis, cm.plasma, cm.inferno, cm.magma, cm.cividis, cm.RdYlGn
	CBI= fig.colorbar(im, orientation='vertical', shrink=0.8)			#make colorbar for the paynting
	plt.show()															#plot
	print( "...done")
	return()
def plot_B_contour():													#-5-#plot contour of |B|(x,z) on xy-plot
	print( "Plot B-countour...")										#
	for ipx in range( 0, len(xp)):										#scan all elements of xp
		for ipy in range( 0, len(yp)):									#scan all elements of yp
			ZP[ipx, ipy]= LA.norm( ZZP[:, ipx, ipy])        			#let Bz [µT] be the value of ZP-axis
	plt.title('|B|(x,y=0,z) [T]')										#set title
	CS= plt.contour( XP, YP, ZP, 10)									#
	plt.show()															#plot
	print( "...done")													#
	return()
def compute_B_combined_contour_and_plot():								#tbd
	print( "Computing...")
	P= np.array( [0., 0., 0.])											#init point of observer
	xp= np.linspace( x_min, x_max, ix_max)  							#x-axis of plot is x-axis of physics
	yp= np.linspace( z_min, z_max, iz_max ) 							#y-axis of plot is z-axis of physics
	XP, YP = np.meshgrid( xp, yp)										#create matrix for XP and YP
	ZP= np.zeros( ( len(xp), len(yp)))									#init ZP-axis of plot
	for ipx in range( 0, len(xp)):										#scan all elements of xp
		for ipy in range( 0, len(yp)):									#scan all elements of yp
			P[0]= XP[ ipx, ipy]											#x of physics is XP of plot
			P[1]= 0.													#y of physics is 0
			P[2]= YP[ ipx, ipy]											#z of physics is YP of plot
			B= B_by_complete_trajectory( i_traj_max, I_traj, P, 1)		#compute total B-vector at P by trajectory#1
			B+= B_by_complete_trajectory( i_traj_max, I_traj, P, 2)		#add of trajectory#2
			ZP[ipx, ipy]= LA.norm( B)        							#let Bz [µT] be the value of ZP-axis
	print( "...done")
	print( "Displaying combined contour-line plot...")
	plt.title('|B|(x,y=0,z) [T]')										#set title
	contours = plt.contour( XP, YP, ZP, 15, colors='black')
	plt.clabel(contours, inline=True, fontsize=8)
	plt.imshow(ZP, extent=( xp[0], xp[ix_max-1], yp[0], yp[iz_max-1]), origin='lower', cmap=cm.viridis, alpha=0.5)
																		#'flag' cm.viridis, cm.plasma, cm.inferno, cm.magma, cm.cividis, cm.RdYlGn, 'RdGy'
	plt.colorbar();
	plt.show()															#plot
	plt.clf																#clear figure
	print( "...done")
	return()
def plot_B_contourf():													#-6-#plot contour of |B|(x,z) on xy-plot
	print( "Plot B-countourf...")										#
	for ipx in range( 0, len(xp)):										#scan all elements of xp
		for ipy in range( 0, len(yp)):									#scan all elements of yp
			ZP[ipx, ipy]= LA.norm( ZZP[:, ipx, ipy]) 		   			#let Bz [µT] be the value of ZP-axis
	plt.title('|B|(x,y=0,z) [T]')										#set title
	CS= plt.contourf( XP, YP, ZP, 100, cmap='RdGy')						#
	plt.colorbar( CS);													#
	plt.show()															#plot
	print( "...done")													#report
	return()															#return
def plot_Bz_surface():													#-7-#plot Bz-surface(x,z) on xyz-plot
	print( "Plot Bz(x,z)-surface...")									#report
	for ipx in range( 0, len(xp)):										#scan all physical x
		for ipy in range( 0, len(yp)):									#scan all physical z
			ZP[ ipx, ipy]= ZZP[ 2, ipx, ipy]							#put Bz(x,z) into z-plot
	ax = plt.axes(projection='3d')										#define 3D-plot
	ax.plot_surface( XP, YP, ZP, cmap='viridis', edgecolor='none')		#define data and colors
	ax.set_title('Bz(x,y=0,z) [T]')										#set title
	plt.show()															#show plot
	print( "...done")													#report
	return()															#return
def create_test_plot():													#OK
	print( "Creating test plot...")										#
	for ipx in range( 0, len(xp)):										#scan all elements of xp
		for ipy in range( 0, len(yp)):									#scan all elements of yp
			ZP[ipx, ipy]= LA.norm( ZZP[:, ipx, ipy])		   			#let Bz [µT] be the value of ZP-axis
	print( "Displaying simple contourf plot...")						#
	CS= plt.contourf( XP, YP, ZP, 100, cmap='RdGy')						#
	plt.colorbar( CS);													#
	plt.show()															#plot
	print( "...done")													#
	return()
def report_B_at_P():													#calculate and report B at all points in the plotting base
	global xp, yp, ZZP, selected_trajectories							#use global vars
	print( "report_B_at_P()...")										#report
	x=0; y=1; z=2														#for convenience
	remaining_trajectories= selected_trajectories						#get local var
	remaining_trajectory_flag= True										#init loop var
	P= np.array( [+0.,+0.,+0.])											#init point of observer
	B= np.array( [+0.,+0.,+0.])											#init B-vector
	for ipx in range( 0, len(xp)):										#scan all elements of xp (physical x)
		for ipy in range( 0, len(yp)):									#scan all elements of yp (physical z)
			P[0]= XP[ ipx, ipy]											#physical x is XP of plot and scanne by ix
			P[1]= 0.													#physical y=0
			P[2]= YP[ ipx, ipz]											#physical z is YP of plot and scanned by iz
			B= np.array( [ 0., 0., 0.])									#init B
			while remaining_trajectory_flag:							#scan all trajectories
				actual_trajectory= eval( remaining_trajectories[ 0:remaining_trajectories.find( ',')])	#get actual trajectory number
				B+= B_by_complete_trajectory( P, actual_trajectory) 	#adding trajectory contributions
				if remaining_trajectories.find( ',') > 0:  					#if there is still some more trajectory
					remaining_trajectories= remaining_trajectories[ remaining_trajectories.find( ',') + 1: ]	#remove actual and make next one active
				else:													#no trajectories left after the actual one, so...
					remaining_trajectory_flag= False					#exit loop next time
			ZZP[:, ipx, ipy]= B											#get vector into ZZP-matrix
			print( "B(",P,")=",ZZP[:, ipx, ipy]," # ", B)				#report result
			key= input()
	print( "...done")
	return()
def compute_B_vectors_in_physical_xz_plane():							#-c-#compute B(x,y=0,z)
	global xp, yp, XP, YP, ZZP, selected_trajectories					#use global vars
	print( "Computing B-vectors(x,y=0,z)...")							#report
	print( "   will give audio signal when finished...")
	P= np.array( [0., 0., 0.])											#init point of observer
	actual_trajectory= 0												#init actual trajectory to dummy value
	for ix in range( 0, len(xp)):										#scan all elements of xp-plot (physical x)
		print( "actual x-index: ", ix, "out of ", len(xp), flush= True)
		for iz in range( 0, len(yp)):									#scan all elements of yp-plot (physical z)
			P[0]= XP[ ix, iz]											#physical x is XP of plot and scanned by ix
			P[1]= 0.													#physical y=0
			P[2]= YP[ ix, iz]											#physical z is YP of plot and scanned by iz
			B= np.array( [ 0., 0., 0.])									#init B
			remaining_trajectories= selected_trajectories + "#"			#get local var
			remaining_trajectory_flag= True								#init loop var
			while remaining_trajectory_flag:
				actual_trajectory= eval( remaining_trajectories[ 0:remaining_trajectories.find( ',')]); 	#get actual trajectory number
				if remaining_trajectories.find( ',') > 0:  				#if there is still some more trajectory
					remaining_trajectories= remaining_trajectories[ remaining_trajectories.find( ',') + 1: ]	#remove actual and make next one active
				else:													#no trajectories left after the actual one, so...
					remaining_trajectories= "none"
					remaining_trajectory_flag= False					#exit loop next time
				#print( "remaining trajectories: ", remaining_trajectories)
				#print( "actual    trajectory  : ", actual_trajectory)
				#print( "-----------------------")
				B+= B_by_complete_trajectory( P, actual_trajectory) 	#adding trajectory contributions
			ZZP[:, ix, iz]= B											#get vector into ZZP-matrix
	print( "...done\a", flush= True)													#report and chime
	return()															#return
def adjust_global_vars():												#needed in case the coordinates are changed
	global x_min, x_max, ix_max, z_min, z_max, iz_max, xp, yp, XP, YP, ZP, ZZP
	print( "Adjust global vars...")
	xp= 		np.linspace( x_min, x_max, ix_max)  					#x-axis of plot is physical x
	print( "xp:"); print( xp)
	yp= 		np.linspace( z_min, z_max, iz_max ) 					#y-axis of plot is physical z
	print( "yp:"); print( yp)
	XP, YP = 	np.meshgrid( xp, yp)									#create matrix for XP and YP
	print( "XP:"); print( XP)
	print( "YP:"); print( YP)
	print( "len(xp): ", len(xp))
	print( "len(yp): ", len(yp))
	print( "XP[0,1]:", XP[ 0,1])
	print( "YP[1,0]:", YP[ 1,0])
	ZP= 		np.zeros( ( len(xp), len(yp)))							#init ZP-axis of plot
	ZZP= 		np.zeros( ( 3, len(xp), len(yp)))						#init ZP-axis of plot (with vector components)
	print( "...done.")
	return()
def my_keypress():														#my os-specific module to get a keypress
	if opsys == "WINDOWS":
		key= ms.getch()													#get from ms the sequence of the keypress
		key= key.decode( 'utf-8')										#convert byte-representation of char to char
	else:																#fuer andere Betriebssysteme (mit ENTER abschliessen!)
		key= input()													#
	print( key)															#report
	return( key)														#return single letter
def my_cls(): 															#my way to clear secreen
	print( "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
	return()
#main routine###########################################################
# vars...
selected_trajectories=  "0,1,2,3"										#string containing the numbers of trajectories to consider
no_sections_traj=		100 											#set number of sections on trajectory of current
I_traj=					1E5												#set trajectory current [A]
ix_max=					20												#set grid points in x-direction
iz_max=					ix_max											#set grid points in z-direction
x_min=					-math.pi/10.									#set min of x
x_max=					-x_min  										#set max of x
z_min=					-0.5											#set min of z
z_max=					+0.5											#set max of z
# prepare global vars...
xp= 		np.linspace( x_min, x_max, ix_max)  						#x-axis of plot is x-axis of physics
yp= 		np.linspace( z_min, z_max, iz_max ) 						#y-axis of plot is z-axis of physics
XP, YP = 	np.meshgrid( xp, yp)										#create matrix for XP and YP
ZP= 		np.zeros( ( len(xp), len(yp)))								#init ZP-axis of plot
ZZP= 		np.zeros( ( 3, len(xp), len(yp)))							#init ZP-axis of plot
# main loop of program..................................................
while True:
	my_cls()															#clear screen
	print( "==========================================================")
	print( "This is '",this_program,"'...")
	print( "MAIN MENUE  (physical y=0!)")
	print( "==========================================================")
	print( "0=quit")
	print( "p-parameters")
	print( "c=compute B vectors in physical xz-plane")
	print( "1=plot Bz(<x>,y=0,z)")
	print( "2=plot Bx,y,z(x,y=0,<z>)")
	print( "3=plot Bx,y,z(<x>,y=0,z)")
	print( "4=plot B-contour & fill by image (|B| in physical xz-plane on xy-plot)")
	print( "5=plot B-contour (|B| in physical xz-plane on xy-plot)")
	print( "6=plot B as filled contour")
	print( "7=plot Bz-surface in xy-plane")
	print( "v=plot B-vector (Bx,Bz) in physical xz-plane")
	print( "t=to test selected modules and functionalities only")
	key= my_keypress()
	if key =='0': break
	elif key == 'p': parameters_menue()									#OK
	elif key == 'c': compute_B_vectors_in_physical_xz_plane()			#OK
	elif key == '1': plot_Bz_vs_z()										#OK
	elif key == '2': plot_B_vs_x()										#OK
	elif key == '3': plot_B_vs_z()										#OK
	elif key == '4':
		my_cls()
		print( "Be aware to use the mouse keys in the plot - otherwise the module will crash!!!")
		input()
		plot_B_contour_and_fill_by_image()					#OK#|B|(x,z) on xy-plot
	elif key == '5': plot_B_contour()									#OK#|B|(x,z) on xy-plot
	elif key == '6': plot_B_contourf()									#OK#|B|(x,z) on xy-plot
	elif key == '7': plot_Bz_surface()									#OK#Bz-surface in physical xz-plane on xyz-plot
	elif key == 'v': plot_B_vector()									#plot Bx,Bz-vector in physical xz-plane
	elif key == 't':													#for testing only
		report_B_at_P()													#check B-vector at point P
		#create_test_plot()												#OK
########################################################################
#EOF
