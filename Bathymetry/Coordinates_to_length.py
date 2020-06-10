# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:09:59 2020

Calculating distance between coordinates using geopy

@author: SSchurer
"""


from geopy.distance import geodesic

# #After rain
# one   = (-14.99405083,	30.216548)
# two   = (-14.99404967,	30.21659917)
# three = (-14.994139, 	30.21655233)
# four  = (-14.99413267,	30.21660117)
# five  = (-14.99421583,	30.21655433)
# six   = (-14.99420783,	30.21660217)

# segment12 = (geodesic(one, two).meters)
# segment13 = (geodesic(one, three).meters)
# segment24 = (geodesic(two, four).meters)
# segment34 = (geodesic(three, four).meters)
# segment35 = (geodesic(three, five).meters)
# segment46 = (geodesic(four, six).meters)
# segment56 = (geodesic(five, six).meters)
# segment26 = (geodesic(two, six).meters)
# segment15 = (geodesic(one, five).meters)

# print(((121/segment12) + (117/segment34) + (117/segment56) + (362/segment26) + (383/segment15))/5)


#------------------------------------------------------------------------------ 
#Before rain
# one   = (-14.99448083,  30.216586)
# two   = (-14.994479,    30.2166445)
# three = (-14.99457983,  30.216595)
# four  = (-14.994578,    30.21664833)
# five  = (-14.994668,    30.21660817)
# six   = (-14.9946675,   30.21665417)

# segment12 = (geodesic(one, two).meters)
# segment13 = (geodesic(one, three).meters)
# segment24 = (geodesic(two, four).meters)
# segment34 = (geodesic(three, four).meters)
# segment35 = (geodesic(three, five).meters)
# segment46 = (geodesic(four, six).meters)
# segment56 = (geodesic(five, six).meters)
# segment26 = (geodesic(two, six).meters)
# segment15 = (geodesic(one, five).meters)

# print(segment26)
# print(689/segment26)
# print(((235/segment12) + (222/segment34) + (195/segment56) + (689/segment26) + (696/segment15))/5)


#------------------------------------------------------------------------------
# #Tracers
# one   = (-14.99355989,	30.21650766)
# two   = (-14.99356858,	30.21646741)
# three = (-14.99363178,	30.2165292)
# four  = (-14.99363876,	30.21648696)
# five  = (-14.99369071,	30.21654201)
# six   = (-14.99370214,	30.21649971)

# segment12 = (geodesic(one, two).meters)
# segment13 = (geodesic(one, three).meters)
# segment24 = (geodesic(two, four).meters)
# segment34 = (geodesic(three, four).meters)
# segment35 = (geodesic(three, five).meters)
# segment46 = (geodesic(four, six).meters)
# segment56 = (geodesic(five, six).meters)
# segment26 = (geodesic(two, six).meters)
# segment15 = (geodesic(one, five).meters)

# print(segment26)
# print(438/segment26)
# print(((134/segment12) + (139/segment34) + (144/segment56) + (438/segment26) + (431/segment15))/5)

#------------------------------------------------------------------------------
#After rain
# one   = (-14.99441326,	30.21655562)
# two   = (-14.993764180,	30.216521769)
# three = (-14.994352039,	30.217727251)


# segment12 = (geodesic(one, two).meters)
# segment13 = (geodesic(one, three).meters)
# segment23 = (geodesic(two, three).meters)

# print('segment12:', segment12)
# print('segment13:', segment13)

#-----------------------------------------------------------------------------

#length RTK track
N = (-14.990527786666709, 30.21521126666666)
S = (-14.994251456666728, 30.2166069)

#Boundary conditions
LeftNorth      = (-14.95273631113323, 30.20313130433327)
LeftMiddleHigh = (-14.990822064738428, 30.21359162917786)
LeftMiddleLow  = ( -14.99533613290174, 30.2139671421182)
LeftSouth       = (-15.033451491103921, 30.224264682470466)

#Width grid
Left  = (-14.993983853361028, 30.213330792373622)
right = (-14.993111075071816, 30.218262204736085)

#Length grid
north = (-14.951998054087035, 30.206585525610368)
south = (-15.033443029183413, 30.224230033841916)

#Length obs grid
one = (-14.993789847345631, 30.216620560822502)
two = (-14.993852627919079, 30.216635302980695)

d =  (-14.993796063402067, 30.216614821653128)
dd = (-14.993859504109988, 30.216632584409304)

d1 = (-14.993470056536735, 30.216544705557705)
d2 = (-14.993533497243572, 30.21656246828266)

left   = (-14.994821484483197, 30.21774733517885)
middle = (-14.994871523775693, 30.216668828159)
right  = (-14.994993221024703, 30.21406552499092)

s1 = (-14.995141814476245, 30.213661168782902)
s2 = (-14.995467821533103, 30.213731280426273)

k1 = (-14.994247563634042, 30.21660693484955)
k2 = (-15.033313719840274, 30.22472752142685)
segmentC1 = (geodesic(k1, k2).meters)

print('segmentC1:', segmentC1)
