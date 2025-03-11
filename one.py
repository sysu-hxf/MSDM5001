# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 20:25:31 2021

@author: DELL
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
#from matplotlib import cm
#from matplotlib import colors

def read_FY4(nom,cal):
    ref = np.zeros(np.shape(nom))+(-999.0)
    loc = np.where(nom<4096)
    ref[loc] = cal[nom[loc]]
    return ref
def get_refs(FY4_file,GEO_file):
    f = h5py.File(FY4_file,'r')
    nom10 = np.array(f['NOMChannel10'][:])
    cal10 = np.array(f['CALChannel10'][:])
    nom13 = np.array(f['NOMChannel13'][:])
    cal13 = np.array(f['CALChannel13'][:])
    nom12 = np.array(f['NOMChannel12'][:])
    cal12 = np.array(f['CALChannel12'][:])
    ref10 = read_FY4(nom10,cal10)
    ref12 = read_FY4(nom12,cal12)
    ref13 = read_FY4(nom13,cal13)
    f.close()
    g = h5py.File(GEO_file, 'r')
    lon = np.array(g['pixel_longitude'][:])
    lat = np.array(g['pixel_latitude'][:])
    loc = np.where((lon< -179) | (lon > 179.) | (lat< -79.) | (lat > 79.))
    lon[loc] = np.nan
    lat[loc] = np.nan
    g.close()
    print ('************')
    return  lon, lat,ref10,ref12,ref13

def get_cloud(lat,lon,ref10,ref12,ref13):
    btdred = ref10 - ref12
    btddiv = ref12 - ref13
    tbb = ref12.copy()
    
    clat,clon = lat.copy(),lon.copy()
    loc = np.where(ref12 < 0 )
    ref12[loc] = np.nan
    
    loc_dcc=np.where((tbb>=240)|(btdred<=-2)|(btddiv>=3))
    tbb[loc_dcc]=np.nan
    return clon,clat,tbb,ref12



def color(m,clat,clon,tbb):
    x2, y2 = m(clon, clat)
    p2 = m.pcolor(x2, y2, tbb, cmap=plt.cm.get_cmap('jet'))
    cbar = m.colorbar(p2)
    p2.set_clim(vmin=180, vmax=240)
    cbar.ax.tick_params(labelsize=12)

def drive_picture(lat,lon,clat,clon,ref12,tbb):
    plt.figure(figsize=(8,8))
    m = Basemap( llcrnrlon = 20., llcrnrlat = -79., urcrnrlon = 179., urcrnrlat = 79.,projection = 'cyl',satellite_height = 35786000,lat_0=0,lon_0=104.5,resolution='l')
    m.shadedrelief(scale =0.5)
    #m=Basemap(projection='ortho',lat_0=0, lon_0=100,resolution='l',satellite_height=10000000)
    m.drawcoastlines(color = 'green')
    m.drawstates(color = 'green')
    m.drawcountries(color = 'green')
    m.drawparallels(np.arange(-79,79,20),labels = [1,0,0,0],fontsize = 12)
    m.drawmeridians(np.arange(20,179,15),labels = [0,0,0,1],fontsize = 12)
    #x1,y1 = m(lon,lat)
    #m.pcolor(x1,y1,ref12,cmap =plt.cm.get_cmap('bone') )
    color(m,clat,clon,tbb)
    '''
    listf = file2.split('_')
    timeini = listf[9]
    timefin = listf[10]
    dpi = listf[11]
    name = timeini +'——'+timefin+'——'+dpi+'深对流云'
    plt.title(name,fontsize=14)
    
    plt.show()  
    '''

if __name__=='__main__':
    file1 =r"H:\data\navigation\GEO.FengYun-4A.xxxcgms.4000M.104DEG.HDF5"
    file2 = r'H:\data\FY4A-_AGRI--_N_DISK_1047E_L1-_FDI-_MULT_NOM_20180915000000_20180915001459_4000M_V0001.HDF'
    lon,lat,ref10,ref12,ref13= get_refs(file2, file1)
    clon,clat,tbb,ref12 = get_cloud(lat,lon,ref10,ref12,ref13)
    drive_picture(lat,lon,clat,clon,ref12,tbb)
