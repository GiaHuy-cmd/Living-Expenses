def tien_dien(kdien):
    if kdien <= 50:
        tien = kdien * 1984
    elif kdien <= 100:
        tien = 50*1984 + (kdien-50)*2050
    elif kdien <= 200:
        tien = 50*1984 + 50*2050 + (kdien-100)*2380
    elif kdien <= 300:
        tien = 50*1984 + 50*2050 + 100*2380 + (kdien-200)*2998
    elif kdien <= 400:
        tien = 50*1984 + 50*2050 + 100*2380 + 100*2998 + (kdien-300)*3350
    else:
        tien = 50*1984 + 50*2050 + 100*2380 + 100*2998 + 100*3350 + (kdien-400)*3460
    return tien
def tien_nuoc(knuoc):
    if knuoc <= 4:
        tien = knuoc * 6700
    elif knuoc <= 6:
        tien = 4*6700 + (knuoc-4)*12900
    else:
        tien = 4*6700 + 6*12900 + (knuoc-6)*14400
    return tien
