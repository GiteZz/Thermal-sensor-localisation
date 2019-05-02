from PIL import Image, ImageDraw

def get_bounding_box(co):
    c_width = 4
    x1 = co[0] - c_width
    x2 = co[0] + c_width
    y1 = co[1] - c_width
    y2 = co[1] + c_width

    return [x1, y1, x2, y2]

def invert(co1, co2):
    width = 750
    height = 477
    n_co1 = (width - co1[1], height - co1[0])
    n_co2 = (width - co2[1], height - co2[0])
    return n_co1, n_co2

cal_points = ((370,407),(320,380),(270,357),(240,335),(200,311),(160,237),(110,259),(150,378),(200,355),(220,346),(260,328),(330,295))
meas_points = ((355,404),(324,383),(273,355),(230,325),(188,290),(145,270),(112,250),(142,353),(189,348),(200,336),(254,327),(333,295))

img_file = '../../GUI/static/Img/layout.png'

img = Image.open(img_file)

d = ImageDraw.Draw(img)

for cal_point, meas_point in zip(cal_points, meas_points):
    cal_point, meas_point = invert(cal_point, meas_point)
    box1 = get_bounding_box(cal_point)
    d.ellipse(box1, fill=(0,0,0))
    box2 = get_bounding_box(meas_point)
    d.ellipse(box2, fill=(255,255,0))
    d.line([cal_point, meas_point],width=2, fill=(0,0,0))

img.show()