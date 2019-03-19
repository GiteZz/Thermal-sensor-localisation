from help_module.localisation_helper import Localiser

#scenario 1 (hoek=0)
center=[500,200]
corner=[336.1696,85.2847]
l=Localiser();
l.set_heigt(380)
l.set_corner_and_center(corner,center)
l.centroids=[[0,0],[300,200]]
ret=l.get_abs_locations()
print(ret)
print("------------")
#scenario 2
center=[500,200]
corner=[318.52,115.2254]
l=Localiser();
l.set_heigt(380)
l.set_corner_and_center(corner,center)
print('error:'+str(l.get_error()))
l.centroids=[[0,0],[300,200]]
ret=l.get_abs_locations()
print(ret)