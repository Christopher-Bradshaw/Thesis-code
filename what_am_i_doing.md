# Doing?

I am comparing how the results from comparing different methods of galaxy growth result in different results

# How am I doing this?

## Zfourge

* This takes a number of deep observations, bins them by redshift and constructs the SMF for each redshift
* This raw data is found in helpers.data.smf
* This data can also be fit to a schechter function and is done by the Zfourge people
* The single and double schechter params are in helpers.data.schechter


* If you want to see this data, run growth_zfourge.py
* That will give graphs of both the raw data and the fitted data


## Paramaterization

* This z fourge data is nice, but has some irregularities.
* We would like to paramaterize the schechter function to get rid of these.
* Joel does this in his paper (saved as paramaterization)
* This is a paramaterization of the schechter functions based on Z
  * a_1 and a_2 are constants (What are these?)
  * Phi_1 and phi_2 vary with z, as does M<sup>*</sup> and M<sub>dot</sub>
* Using this paramaterization with the Zfourge data, we have a nice set of data for far away things

##


# Details

## What is a schechter function?

* See [Virginia astro class on them](https://www.astro.virginia.edu/class/whittle/astr553/Topic04/Lecture_4.html)
* Paul Schechter (1974) looked at the mass distribution of galaxies. Found that this function fit well. Why? Who knows


# Code?

## Main

### zfourge_smf
* Plots a variety of graphs showing the **SMF** based on
  1. The raw Zfourge data
  2. The schechter funcs derived from the Zfourge data
  3. The paramaterized Schechter funcs from Joel

### mass_const_num_den
* Plots a single graph showing the change in mass at constant number density of time
* Uses the paramaterization
* Uses various start masses, and tracks the mass at the number density over time
