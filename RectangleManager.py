import math
import DataContainer as DC

VList = list()
HList = list()
VstartList = list()
HstartList = list()


def get3Ddist(m1,m2):
    mx = (m1.x -m2.x) ** 2
    my = (m1.y -m2.y) ** 2
    mz = (m1.z -m2.z) ** 2
    return(math.sqrt(mx + my + mz))



# found_bmi_range = [bmi_range for bmi_range
#                    in bmi_ranges
#                    if bmi_ranges[2] <= bmi <= bmi_ranges[3]
#                   ][0]
def createLines(rows):
    global VList, HList
    try:
        # each point in column
        for  row in rows:
            point = row
            isline = False
            if VList:
                isline = [p for p in VList 
                    if ((p[1] <= point.vnewdeg <= p[2] ) and p[0] == point.hnewdeg)][0]
            if not isline:
                pass
    except Exception as exc:
        print("createLines : " + exc)
        


def searchRectangles(mrows,mcols,targetwidth, targetheight):
    # initial pass
    for k in mrows.keys():
        createLines(mrows[k])
    pass

def createRectangles(targetwidth, targetheight):
    global HList, VList,VstartList, HstartList

    mrows, mcols = DC.sortRows()

    VList = list()
    HList = list()
    VstartList = list()
    HstartList = list()


    searchRectangles(mrows,mcols,targetwidth, targetheight)    
