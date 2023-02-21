#Shannon Curley
#Final Project
#Question 2 - Choropleth mapping
'''
Purpose Statement:
    This program creates choropleth maps with quantitative data from
    shapefiles. It makes use of 2 classification methods (equal interval
    and quantile) and 3 color schemes from colorbrewer2.org.
    Each run of the program requires user inputs for: shapefile, attribute
    to map, number of classes, classification method, and color scheme.

Name: Shannon Curley
'''

#Needed imports

import sys
sys.path.append(r'C:\Users\shanc\Documents\ohio_state\GIS_programming\gisalgs')
from geom.shapex import *
from xcolorbrewer import *

import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch

#Functions for obtaining attribute, class, and color information
def att_choice(num_atts):
    '''
    This function asks users to choose an attribute for mapping
    from a predetermined list.
    
    Input:
        a list of numerical attributes from a shapefile
    Output:
        map_att - one user selected attribute
    '''

    print("""
    This program maps only numerical data and uses
    sequential color schemes for visualization.
    The following list shows the numerical attributes
    in your shapefile.
            """)
    print('The fields are: ')
    for i in range(len(num_atts)):
        print(f"{i:>5}", f"{num_atts[i]:>15}")

    print("""
    Please type in the number from above that represents the
    attribute you want to map. If "OBJECTID" or "SHAPELENGTH"
    or something similar representing those attributes 
    are in the options list, it is not recommended you choose
    them because it will not create a meaningful map.

    This program is best suited to attributes related to
    area, population, or similar phenomena.

    If your shapefile does not have attributes like this or
    contains only one polygon, choose a different shapefile
    and restart the program.
    """)

    while is_polygon_shp == True:
        try:
            inp = input("Choose an attribute:")
            if int(inp) in range(len(num_atts)):
                map_att = num_atts[int(inp)]
                break
            else:
                print('Please type only a digit shown to the left of an attribute.')
                continue
        except Exception as e:
            print('Error:', e)
            print('Make sure you enter only the representative digit')
    
    return map_att

def cl_def():
    '''
    This function prompts a user to select the
    number of classes they want.
    '''

    print("""
    The data needs to be split into classes.
    The minimum number of classes is 3
    and the maximum is 9.
    """)
    
    while is_polygon_shp == True:
        try:
            inp = input("How many data classes do you want? (3-9)")
            if int(inp) in range(3, 10):
                cl_num = int(inp)
                break
            else:
                print('Please type only a digit in range such as "4" or "9".')
                continue
        except Exception as e:
            print('Error:', e)
            print('Make sure you enter only a single digit')
    
    return cl_num

def colorchoice():
    '''
    This function provides users with a list of 3 color
    schemes based on colorbrewer2.org and asks them to
    choose one for mapping.
    '''
    
    print("""
    There are 3 sequential color options.
        Option 1: blues (single hue)
        Option 2: yellow, orange, red
        Option 3: red to purple
    """)

    while is_polygon_shp == True:
        try:
            colorop = input("Please choose a color scheme (1, 2, or 3):")
            if int(colorop) == 1:
                choice = "Blues"
                break
            elif int(colorop) == 2:
                choice = "YlOrRd"
                break
            elif int(colorop) == 3:
                choice = "RdPu"
                break
            else:
                if colorop != '1' or colorop != '2' or colorop != '3':
                    print('Please type only the digit "1", "2" or "3".')
                    continue
        except Exception as e:
            print('Error:', e)
            print('Make sure you enter only the 1, 2, or 3')
    
    return choice

def cl_method(values, cl_num):
    '''
    This function contains the code to classify data based on
    equal interval and quantile classification methods.
    Users are prompted to select a method.
    
    Input:
        values - a list of numerical values
        cl_num - the user selected class number
    
    Output:
        val_classes - a list containing an integer for each value's class
        (same order as original values list)
        info - contextual information based on each classification type
        (class breaks for eq. interval, # of values in each class for quantile)
    '''

    print("""
    This program has 2 classification method options.
    """)
    print("""
    Option 1: equal interval
    (each class spans an equal range of data)

    Option 2: quantile
    (each class contains approx. the same number of features)
    """)

    while is_polygon_shp == True:
        try:
            cl_meth = input("Please choose a method (1 or 2):")
            
            if int(cl_meth) == 1:
                #equal interval
                sort_vals = sorted(values)

                cl_range = (sort_vals[-1] - sort_vals[0])/cl_num

                cl_bounds = [(i * cl_range)+ sort_vals[0] for i in range(1, cl_num+1)]

                info = "Class breaks:", cl_bounds
                    
                val_classes = []

                for v in values:
                    if v <= sort_vals[0] + cl_range:
                        val_classes.append(0)
                        continue
                    b = 0
                    while b < cl_num-1:
                        b += 1
                        if v > sort_vals[0] + (cl_range*b) and v <= sort_vals[0] + (cl_range*(b+1)):
                            val_classes.append(b)
                            break
                        else:
                            b += 1
                            if v > sort_vals[0] + (cl_range*b) and v <= sort_vals[0] + (cl_range*(b+1)):
                                val_classes.append(b)
                                break
                break
            
            elif int(cl_meth) == 2:
                #quantile
                val_ind = [[values[i], i] for i in range(len(values))]
                
                sort_vals = sorted(val_ind)

                quant_num = len(values) / cl_num

                info = "Approx. # of features in each class:", int(quant_num)

                for i in range(len(sort_vals)):
                    v = sort_vals[i]      

                    if i <= quant_num-1:
                        v.append(0)
                        continue
                    b = 0
                    while b < cl_num:
                        b += 1
                        if i > (quant_num-1)*b and i <= (quant_num*(b+1))-1:
                            v.append(b)
                            break
                        else:
                            b += 1
                            if i > (quant_num-1)*b and i <= (quant_num*(b+1))-1:
                                v.append(b)
                                break
                sort_val_classes = sorted(sort_vals, key=lambda v: v[1])

                val_classes = [i[2] for i in sort_val_classes]

                break

            else:
                if cl_meth != '1' or cl_meth != '2':
                    print('Please type only the digit "1" or "2"')
                    continue
        except Exception as e:
            print('Error:', e)
            print('Make sure you enter only 1 or 2.')

    
    return val_classes, info 


#Functions for drawing the polygons

def make_path(polygon):
    '''Creates a matplotlib path for a polygon that may have holes.
    
    This function requires to import the following modules
       from matplotlib.path import Path
       from matplotlib.patches import PathPatch

    Input: 
       polygon     [ [ [x,y], [x,y],... ],    # exterior
                     [ [x,y], [x,y],... ],    # first interior ring (optional)
                     [ [x,y], [x,y],... ],   # second interior ring (optional)
                     ... ]                   # there can be more rings (optional)
    Output:
       path: a Path object'''
    
    def _path_codes(n):
        codes = [Path.LINETO for i in range(n)]
        codes[0] = Path.MOVETO
        return codes

    verts = []
    codes = []
    for ring in polygon:
        verts.extend(ring)
        codes += _path_codes(len(ring))
    return Path(verts, codes)

def draw_polygon(polygon, color):
    '''
    This is an edited version of the same function from
    our course materials. Some of the original function's
    code is still here, and other parts are in the
    program code.
    '''
    xcoords = [p[0] for p in polygon[0]]
    xmin = min(xcoords)
    xmax = max(xcoords)
    ycoords = [p[1] for p in polygon[0]]
    ymin = min(ycoords)
    ymax = max(ycoords)
    xmin, xmax, ymin, ymax

    path1 = make_path(polygon)
    patch = PathPatch(path1, facecolor= color, edgecolor= 'none')
    ax.add_patch(patch)

#Shapefile input from user

is_polygon_shp = False
while not is_polygon_shp:
    fname = input("Enter a shapefile name: ")
    #fname = r'C:/Users/shanc/Documents/ohio_state/GIS_programming/final_proj/testing/nys_counties/cugir-007865/cty036.shp'
    try:
        mapdata = shapex(fname)
    except Exception as e:
        print('Error:', e)
        print('Make sure your enter a valid shapefile')
        continue
    shp_type = mapdata[0]['geometry']['type']
    if shp_type in ['Polygon', 'MultiPolygon']:
        is_polygon_shp = True
    else:
        print('Make sure it is a polygon or multipolygon shapefile')
    print()  

shp = shapex(fname)

#Selects out the features that are numerical

f = shp[0]          #Sample feature to obtain the numerical atts

num_atts = []
for a in f['properties']:
    if type(f['properties'][a]) == int or type(f['properties'][a]) == float:
        num_atts.append(a)
    else:
        continue

map_att = att_choice(num_atts)

#Places the values of map_att into a list for classification purposes

values = []

for i in range(len(shp)):
    f = shp[i]
    values.append(f['properties'][map_att])

#Defines number of classes and uses that to sort data via classification method

cl_num = int(cl_def())
results = cl_method(values, cl_num)
val_classes = results[0]

#Creates a color list based on xcolorbrewer file's function

choice = colorchoice()
colors = get_colorbrewer_specs(choice, cl_num)

#Program outputs-- attribute information and map image

print('Mapped attribute:', map_att)
print(results[1][0], results[1][1])

_, ax = plt.subplots()

#assign x/y min/max using first polygon as a basis for comparison
f = shp[0]
xcoords = [p[0] for p in f['geometry']['coordinates'][0]]
xmin = min(xcoords)
xmax = max(xcoords)
ycoords = [p[1] for p in f['geometry']['coordinates'][0]]
ymin = min(ycoords)
ymax = max(ycoords)

for i in range(len(shp)):
    f = shp[i]

    b = val_classes[i]
    color = colors[b]
    
    geom_type = f['geometry']['type']
    if geom_type == 'MultiPolygon':
        for i in range(len(f['geometry']['coordinates'])):      #Draws each part of a multipolygon
            poly = f['geometry']['coordinates'][i]
            draw_polygon(poly, color)
    else:
        poly = f['geometry']['coordinates']
        draw_polygon(poly, color)

    #to get the max/min x and y limits of the whole data set
    xcoords = [p[0] for p in poly[0]]
    nxmin = min(xcoords)
    nxmax = max(xcoords)
    if nxmin < xmin:
        xmin = nxmin
    if nxmax > xmax:
        xmax = nxmax

    ycoords = [p[1] for p in poly[0]]
    nymin = min(ycoords)
    nymax = max(ycoords)
    if nymin < ymin:
        ymin = nymin
    if nymax > ymax:
        ymax = nymax

    xmin, xmax, ymin, ymax

ax.set_ylim([ymin, ymax])
ax.set_xlim([xmin, xmax])

ax.set_aspect(1)
plt.show()
