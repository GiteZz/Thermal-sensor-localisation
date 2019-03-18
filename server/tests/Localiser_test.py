from help_module.localisation_helper import Localiser


center=[100,125]
corner=[100-16,125-12]
l=Localiser();
l.set_corner_and_center(corner,center)
l.centroids=[[12,24],[0,0],[12,26]]
ret=l.get_abs_locations()
print(ret)
