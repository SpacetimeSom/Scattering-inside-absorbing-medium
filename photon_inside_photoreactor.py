
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 17:53:39 2022

@author1: somendrasinghjadon
@author2: kalpakgupta
"""

#%% import modules
import numpy as np
import random

#%% Select scattering parameters
Us=3 #Us of transparent scattering particle
g=0.9 #Anisotropic factor
ua=10 #Ua of the medium

#%% System configuration
totalAbsorption=0 #Total absorbed power
Lz=1; Lx=1E3; Ly=1E3  # System boundaries
itr=int(1E5) #Number of photon packets

#%% Run Monte Carlo simulation
for i in range(0,itr): #Loop over all photon packets
    Ux=0; Uy=0; Uz=1 #Initialize direction cosines
    w=1 #Initialize photon packet weight
    x=0; y=0; z=0 #Initialize coordinate of photon packet
    x_list=[]; y_list=[]; z_list=[] #Position after each scattering event
    
    s=-np.log(random.uniform(0,1))/Us #Photon step size
    x=s*Ux; y=s*Uy; z=s*Uz #Updating photon packet's position

    sys=True
    lim=0
    
    if z>=Lz: #if photon packet reaches the other boundary without scattering
        totalAbsorption+=w*(1-np.exp(-ua*Lz))
    else: #if the photon packet hits a scattering particle inside the system
        totalAbsorption+=w*(1-np.exp(-ua*s))
        w=w*np.exp(-ua*s)
                                                                                
    while 0<z<Lz and sys and w>=0.001: #while photon packet is inside medium
        phi=random.uniform(0,1)*2*3.14 #Calculate azimuthal angle phi
        e=random.uniform(0,1) #Random number for theta
        
        if (abs(g)<0.001): #Find scattering angle theta
            theta = ((2*e)-1)*180/np.pi
        else:
            cos=(1/(2*g))*(1 + g**2 - ((1-g**2)/(1+g*(2*e - 1)))**2)
            theta=np.arccos(cos)

        #Update direction cosines
        sin_theta=np.sin(theta)
        cos_theta=np.cos(theta)
        sin_phi=np.sin(phi)
        cos_phi=np.cos(phi)
        if abs(Uz)>0.99999:
            Uz_1=np.sign(Uz)*cos_theta
            Uy_1=sin_theta*cos_phi
            Ux_1=sin_theta*sin_phi
        else:
            Usqr=np.sqrt(1-Uz**2)
            Uz_1=-sin_theta*cos_phi*Usqr + Uz*cos_theta
            Ux_1=(sin_theta*(Uz*Ux*cos_phi - Uy*sin_phi)/(Usqr)) + Ux*cos_theta
            Uy_1=(sin_theta*(Uz*Uy*cos_phi + Ux*sin_phi)/(Usqr)) + Uy*cos_theta
        Ux=Ux_1; Uz=Uz_1; Uy=Uy_1
        
        s=-np.log(random.uniform(0,1))/Us #Photon step size
        loop=True
        while loop:
            z1=z+s*Uz; x1=x+s*Ux; y1=y+s*Uy #Update photon packet position
            if 0<=z1<=Lz: #If photon packet is inside medium
                x=x1; y=y1; z=z1 #update coordinates of photon packet
                x_list.append(x); y_list.append(y); z_list.append(z)
                totalAbsorption+=w*(1-np.exp(-ua*s)) #Absorbed energy
                w=w*np.exp(-ua*s) #Weight after scattering
                break
            elif z1>Lz: #If packet outside medium in forward direction
                d=abs((Lz-z)/Uz) #Distance from scattering event to boundary
                totalAbsorption+=w*(1-np.exp(-ua*d)) #Absorbed energy
                w=w*np.exp(-ua*d) #Weight (redundant)
                z1=Lz; x1=x+d*Ux; y1=y+d*Uy #update coordinates of photon packet
                x_list.append(x1); y_list.append(y1); z_list.append(z1)
                sys=False #Terminate and launch new packet
                break
            else: #If packet outside medium after backscattering
                d=abs(z/Uz) #Distance from scattering event to boundary
                totalAbsorption+=w*(1-np.exp(-ua*d)) #Absorbed energy
                w=w*np.exp(-ua*d)  #Weight (redundant)
                z=0; x1=x+d*Ux; y1=y+d*Uy #update coordinates of photon packet
                x_list.append(x1); y_list.append(y1); z_list.append(z)
                sys=False #Terminate and launch new packet
                break

        if w<0.001: #Russian roulette if weight goes below threshold
              m=10
              e=random.uniform(0,1)
              if e<=1/m:
                  w=w*m
              else:
                  w=0

print((totalAbsorption/itr)/(1-np.exp(-ua))) #Absorbed energy


