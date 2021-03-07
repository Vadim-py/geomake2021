from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from .forms import Form
from .models import Article, coordinate, Y_coordinate
from shapely.geometry import Point, LineString
from pyproj import Proj, transform

import requests
import matplotlib.pyplot as plt
import numpy as np
import cv2
import math
import geopandas as gpd
import geojson
import folium
import flexpolyline
import os

def index(request):
  path = 'media'
  dir_list = [os.path.join(path, x) for x in os.listdir(path)]
  if dir_list:
    date_list = [[x, os.path.getctime(x)] for x in dir_list]
    sort_date_list = sorted(date_list, key=lambda x: x[1], reverse=True)
    print(sort_date_list[0][0])
  img = cv2.imread(sort_date_list[0][0])
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  gray = np.float32(gray)

  corners = cv2.goodFeaturesToTrack(gray, 1000, 0.0001, 100)
  corners = np.int0(corners)
  squeezed = corners.squeeze().tolist()
  squeezed = corners.squeeze().tolist()

  x_squeezed = np.array([i[0] for i in squeezed])
  y_squeezed = np.array([i[1] for i in squeezed])
  matrix = np.array([x_squeezed, -y_squeezed])
  for index, coord in enumerate(matrix[0]):
    plt.text(coord, matrix[1][index], str(index))

  def distance(P1, P2):
    """
    This function computes the distance between 2 points defined by
     P1 = (x1,y1) and P2 = (x2,y2)
    """
    return ((P1[0] - P2[0]) ** 2 + (P1[1] - P2[1]) ** 2) ** 0.5

  def optimized_path(coords, start=None):
    """
    This function finds the nearest point to a point
    coords should be a list in this format coords = [ [x1, y1], [x2, y2] , ...]
    """
    if start is None:
      start = coords[0]
    pass_by = coords
    path = [start]
    pass_by.remove(start)
    while pass_by:
      nearest = min(pass_by, key=lambda x: distance(path[-1], x))
      path.append(nearest)
      pass_by.remove(nearest)
    return path

  path = optimized_path(squeezed)
  x = np.array([i[0] for i in path])
  y = np.array([i[1] for i in path])

  matrix = np.array([x, -y])

  for index, coord in enumerate(matrix[0]):
    plt.text(coord, matrix[1][index], str(index))
  meters = 10
  if request.method == 'POST':
    form = Form(request.POST, request.FILES)
    if form.is_valid():
      post = form.save(commit=False)
      post.save()
    cor = float(request.POST['x'])
    y_cor = float(request.POST['y'])
    #l = coordinate.objects.latest('x')
    #c = Y_coordinate.objects.latest('y')
    #print(l, c)
    # Координаты в системе координат EPSG:3857
    x_original_point = cor
    y_original_point = y_cor

    mx = x * meters + x_original_point
    my = y * -meters + y_original_point

    inProj = Proj(init='epsg:3857')
    outProj = Proj(init='epsg:4326')
    yu = transform(inProj, outProj, mx, my)
    mxy = list(zip(yu[0], yu[1]))
    picture_df = gpd.GeoDataFrame(
      {'id': range(0, len(mxy))},
      crs="EPSG:3857",
      geometry=[Point(resu) for resu in mxy]
    )

    picture_df.to_file("cat.geojson", driver='GeoJSON', encoding="utf-8")
    SERVICE = 'https://router.hereapi.com/v8/routes?apiKey=JCg7lq0Po2JjlKeoYtVeU-KnjslXB2OYiAqj_Iad_xM&transportMode=pedestrian&return=polyline'
    file = open('cat.geojson')
    data = geojson.load(file).copy()
    file.close()
    coords_list = [feature['geometry']['coordinates'] for feature in data['features']]

    start_point = coords_list[0]
    destination_point = coords_list[len(coords_list) - 1]

    coords_list.remove(start_point)
    coords_list.remove(destination_point)
    origin = f'&origin={start_point[1]},{start_point[0]}'
    destination = f'&destination={destination_point[1]},{destination_point[0]}&'
    waypoints = '&'.join([f'via={coords[1]},{coords[0]}' for coords in coords_list])
    routes = requests.get(SERVICE + origin + destination + waypoints).json()

    def decode(section):
      line = flexpolyline.decode(section['polyline'])
      line = [(coord[1], coord[0]) for coord in line]
      return LineString(line)

    geometry = [decode(section) for section in routes['routes'][0]['sections']]
    route_df = gpd.GeoDataFrame(geometry=geometry)
    route_df.to_file("route.geojson", driver='GeoJSON', encoding="utf-8")
    m = folium.Map(
      #location=[1.90919410026879, 1.736663818359375],
      zoom_start=10,
      tiles='https://1.base.maps.ls.hereapi.com/maptile/2.1/maptile/newest/reduced.day/{z}/{x}/{y}/256/png?lg=RU&apiKey=JCg7lq0Po2JjlKeoYtVeU-KnjslXB2OYiAqj_Iad_xM',
      attr='HERE'
    )

    # folium.GeoJson('cat.geojson', name="geojson").add_to(m)
    folium.GeoJson('route.geojson', name="geojson").add_to(m)
    m.save('geo/templates/map.html')
    return render(request, 'map.html')
  else:
    form = Form()
  return render(request, 'index.html', {'form': form})
