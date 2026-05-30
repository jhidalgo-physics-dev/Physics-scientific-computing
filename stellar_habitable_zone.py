"""
Stellar Habitable Zone Evolution

Author: John Hidalgo

This project analyzes stellar evolution tracks and
models the evolution of habitable zone boundaries
for stars ranging from 0.5 to 1.2 solar masses.

The code calculates stellar luminosity evolution,
habitable zone distances, and stellar lifetimes,
then generates visualizations illustrating how
planetary habitability changes over time.

Developed for:
AST 321 - Stellar Astrophysics
Arizona State University
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D


all_files = ('hr.5A',
             'hr.6A',
             'hr.7A',
             'hr.8A',
             'hr.9A',
             'hr.0A',
             'hr.1A',
             'hr.2A')
#all_files = ('hr.0A')

TEMP_array_hr = []
LUM_array_hr = []
time_array_hr = []
rad_array_hr = []


## Use if statement for one file; use "for" loop for multiple

#if (all_files == 'hr.0A'):
  #file = all_files

for file in all_files:
  stellarModel = open(file, 'r')

  i = 1
  tstep = 0

  dataframe_hr = pd.read_table(stellarModel,sep='\\s+',names=np.arange(14))
  nrows = np.shape(dataframe_hr)[0]

  #Code reads in log(temperature) (T), log(luminosity/Lsol) (L), time in seconds (t), and stellar radius in cm (r).

  T_array_hr = []
  L_array_hr = []
  t_array_hr = []
  r_array_hr = []
  for i in range(nrows):
        if i%19 == 0:
            T_array_hr.append(dataframe_hr[8][i])
            L_array_hr.append(dataframe_hr[7][i])
            t_array_hr.append(dataframe_hr[2][i])
            r_array_hr.append(dataframe_hr[4][i])

  time = np.array(t_array_hr)
  time = time/3600.0/365.0/24.0

  L = np.array(L_array_hr)
  L = 10.0**L

  T = np.array(T_array_hr)
  T = 10.0**T

  rad = np.array(r_array_hr)

  TEMP_array_hr.append(T)
  LUM_array_hr.append(L)
  time_array_hr.append(time)
  rad_array_hr.append(rad)

  stellarModel.close()

#Clean Labels for each stellar track
labels = {
    'hr.5A': '0.5 M☉',
    'hr.6A': '0.6 M☉',
    'hr.7A': '0.7 M☉',
    'hr.8A': '0.8 M☉',
    'hr.9A': '0.9 M☉',
    'hr.0A': '1.0 M☉',
    'hr.1A': '1.1 M☉',
    'hr.2A': '1.2 M☉'
}

#Plot all HR diagrams
for j in range(len(all_files)):
  T = TEMP_array_hr[j]
  L = LUM_array_hr[j]

  logT = np.log10(T)
  logL = np.log10(L)

  plt.figure(figsize=(8,6))
  plt.plot(logT, logL, linewidth=2, label=all_files[j])
  plt.xlabel('log(Temperature) [K]')
  plt.ylabel('log(Luminosity / L☉)')
  plt.title(f'HR Diagram: {all_files[j]} ({labels[all_files[j]]})')
  plt.grid(True)
  plt.legend()
  plt.gca().invert_xaxis()

  plt.show()

#Combined HR Diagram (optional)
plt.figure(figsize=(9,7))

for j in range(len(all_files)):
  T = TEMP_array_hr[j]
  L = LUM_array_hr[j]

  logT = np.log10(T)
  logL = np.log10(L)

plt.plot(logT, logL, linewidth=2, label=f"{all_files[j]} ({labels[all_files[j]]})")
plt.xlabel('log(Temperature) [K]')
plt.ylabel('log(Luminosity / L☉)')
plt.title('Combined HR Diagram for Mass-Varying Stellar Models')
plt.grid(True)
plt.legend()
plt.gca().invert_xaxis()

#Habitable Zone Calculations

#Stellar flux for inner or outer edge of HZ, *must be in Kelvin*

def calculate_seff(Teff, edge):

  T_star = Teff - 5780.0

  if edge == 'inner':
    Seff_sun = 1.107
    a = 1.332E-04
    b = 1.580E-08
    c = -8.308E-12
    d = -1.931E-15

  elif edge == 'outer':
    Seff_sun = 0.356
    a = 6.171E-05
    b = 1.698E-09
    c = -3.198E-12
    d = -5.575E-16

  else:
    raise ValueError("Edge must be either 'inner' or 'outer'")

  Seff = Seff_sun + a*T_star + b*T_star**2 + c*T_star**3 + d*T_star**4

  return Seff

#HZ boundary distance in AU

def calculate_hz_distance(L, Teff, edge):

  Seff = calculate_seff(Teff, edge)
  d_HZ = np.sqrt(L / Seff)

  return d_HZ

#HZ Evolution for Each stellar mass

for j in range(len(all_files)):

  T = TEMP_array_hr[j]
  L = LUM_array_hr[j]
  time = time_array_hr[j] / 1e9

  inner_HZ = calculate_hz_distance(L, T, 'inner')
  outer_HZ = calculate_hz_distance(L, T, 'outer')

  plt.figure(figsize=(8,6))
  plt.plot(time, inner_HZ, linewidth=2, label='Inner HZ Edge')
  plt.plot(time, outer_HZ, linewidth=2, label='Outer HZ Edge')

  plt.xlabel('Time [Gyr]')
  plt.ylabel('Habitable Zone Distance [AU]')
  plt.title(f'Habitable Zone Evolution: {all_files[j]} ({labels[all_files[j]]})')
  plt.grid(True)
  plt.legend()
  plt.show()

#Combined HZ plot

plt.figure(figsize=(10,7))

for j in range(len(all_files)):

  T = TEMP_array_hr[j]
  L = LUM_array_hr[j]
  time = time_array_hr[j] / 1e9

  inner_HZ = calculate_hz_distance(L, T, 'inner')
  outer_HZ = calculate_hz_distance(L, T, 'outer')

  line, = plt.plot(time, outer_HZ, linewidth=2,
           label=f'{labels[all_files[j]]}')
  plt.plot(time, inner_HZ, linestyle='--', linewidth=2, color=line.get_color())

plt.xlabel('Time [Gyr]')
plt.ylabel('Habitable Zone Distance [AU]')
plt.title('Habitable Zone Evolution for Different Stellar Masses')
plt.grid(True)

#custom legend
solid_line = Line2D([0], [0], color='black', linestyle='-', label='Outer HZ')

dashed_line = Line2D([0], [0], color='black', linestyle='--', label='Inner HZ')

#Stellar Mass legend
legend1 = plt.legend(fontsize=8, ncol=2, loc='upper right')

#linestyles
legend2 = plt.legend(handles=[solid_line, dashed_line], loc='upper left')

plt.gca().add_artist(legend1)

plt.show()


#Calculating stellar lifetimes

mass_values = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2])

stellar_lifetimes = []

for j in range(len(all_files)):

  time_gyr = time_array_hr[j] / 1e9
  lifetime = np.max(time_gyr)

  stellar_lifetimes.append(lifetime)

stellar_lifetimes = np.array(stellar_lifetimes)

plt.figure(figsize=(8,6))
plt.plot(mass_values, stellar_lifetimes, marker='o', linewidth=2)
plt.xlabel('Stellar Mass [Msun]')
plt.ylabel('Approximate Stellar Lifetime [Gyr]')
plt.title('Stellar Lifetime vs Stellar Mass')
plt.grid(True)
plt.show()
