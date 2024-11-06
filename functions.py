import numpy as np
import dearpygui.dearpygui as dpg
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import csv

from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


table = np.array([], dtype=object)
row_selected = np.array([], dtype=np.int64)
plot_locations_texture = np.full((2500*2500*4), 1, dtype=np.float32) 


def search(sender, appdata, userdata) -> None:
  """
  SEARCH EVENTS AND UPDATE AND DISPLAY IT
  """

  dpg.hide_item("window_search")
  notification("Loading.... Meanwhile go to eat a cookie....", title="Loading")

  global table, row_selected
  row_selected = np.array([], dtype=np.int64)

  #REMOVE ALL ROWS
  for i in range(len(table)):
    dpg.delete_item(f"row_{i}")

  values = np.array( dpg.get_values
               (
                 [
                    userdata["starttime.year"], #0
                    userdata["starttime.month"], #1
                    userdata["starttime.day"], #2
                    userdata["starttime.time"], #3 {'sec': 0, 'min': 0, 'hour': 0, 'month_day': 0, 'month': 0, 'year': 0, 'week_day': 0, 'year_day': 0, 'daylight_savings': 0}
                    userdata["endtime.year"], #4
                    userdata["endtime.month"], #5
                    userdata["endtime.day"], #6
                    userdata["endtime.time"], #7
                    userdata["minmagnitude"], #8
                    userdata["maxmagnitude"], #9
                    userdata["latitude"], #10
                    userdata["longitude"], #11
                    userdata["minradius"], #12
                    userdata["maxradius"], #13
                    userdata["mindepth"], #14
                    userdata["maxdepth"], #15
                    userdata["limit"], #16
                    userdata["orderby"] #17
                  ]
                ), dtype=object
              )

  starttime = UTCDateTime(
    year=int(values[0]),
    month=int(values[1]),
    day=int(values[2]),
    hour=int(values[3]["hour"]),
    minute=int(values[3]["min"]),
    second=int(values[3]["sec"])
    )

  endtime = UTCDateTime(
    year=int(values[4]),
    month=int(values[5]),
    day=int(values[6]),
    hour=int(values[7]["hour"]),
    minute=int(values[7]["min"]),
    second=int(values[7]["sec"])
    )

  #IF ANY VALUE IS NULL OR WATHEVER 
  for i, v in enumerate(values):
    if v in [None, "", 0, "None"]:
      values[i] = None

  client = Client()
  events = None

  try:
    events = client.get_events(starttime=starttime,
                               endtime=endtime,
                               minmagnitude=values[8],
                               maxmagnitude=values[9],
                               latitude=values[10],
                               longitude=values[11],
                               minradius=values[12],
                               maxradius=values[13],
                               mindepth=values[14],
                               maxdepth=values[15],
                               limit=values[16],
                               orderby=values[17]
                              )

  except Exception as ex:
    notification(msg=ex, title="Error", can_close=True)
    return

  update_GUI(events)


def update_GUI(events) -> None:
  """
  UPDATE THE GUI
  """

  global table
  table = np.empty((len(events), 10), dtype=object)

  for i, event in enumerate(events):
    #y, x
    table[i][0] = i #id
    table[i][1] = event.preferred_origin()["creation_info"].author
    table[i][2] = UTCDateTime(event.preferred_origin()["time"].datetime)
    table[i][3] = event["event_type"]

    ed = [ f"(Text:{v.text} Type:{v.type})" for v in event.get("event_descriptions") ]
    table[i][4] = ", ".join(ed)

    table[i][5] = event.preferred_origin()["latitude"]
    table[i][6] = event.preferred_origin()["longitude"]
    table[i][7] = event.preferred_origin()["depth"]
    table[i][8] = event.preferred_magnitude()["mag"]
    table[i][9] = event.preferred_magnitude()["magnitude_type"]

    with dpg.table_row(parent="window_main_table_info", tag=f"row_{i}"):
      dpg.add_selectable(label=f"{table[i][0]}", span_columns=True, user_data=i, callback=selected)
      dpg.add_selectable(label=f"{table[i][1]}", span_columns=True, user_data=i, callback=selected)
      dpg.add_selectable(label=f"{table[i][2]}", span_columns=True, user_data=i, callback=selected)
      dpg.add_selectable(label=f"{table[i][3]}", span_columns=True, user_data=i, callback=selected)
      dpg.add_selectable(label=f"{table[i][4]}", span_columns=True, user_data=i, callback=selected)
      dpg.add_selectable(label=f"{table[i][5]}", span_columns=True, user_data=i, callback=selected)
      dpg.add_selectable(label=f"{table[i][6]}", span_columns=True, user_data=i, callback=selected)
      dpg.add_selectable(label=f"{table[i][7]}", span_columns=True, user_data=i, callback=selected)
      dpg.add_selectable(label=f"{table[i][8]}", span_columns=True, user_data=i, callback=selected)
      dpg.add_selectable(label=f"{table[i][9]}", span_columns=True, user_data=i, callback=selected)

  #PLOT MAGNITUDES
  mg = set(table[:, 9])
  dpg.configure_item("window_plot_magnitudes_selector", items=list(mg))

  #PLOT WAVES
  #dpg.add_input_int(label="event (by id)", tag="window_plot_wave_id")
  #dpg.configure_item("window_plot_wave_id", max_value=len(table)-1)

  notification("", show=False) #HIDE NOTIFICATION


def notification(msg:str|None, title:str="", show:bool = True, can_close:bool = False) -> None:
  """
  SHOW ANY NOTIFICATION
  """

  dpg.set_value("window_notification_label", value=msg)
  dpg.configure_item(item="window_notification", label=title, no_close=(not can_close))

  if show:
    dpg.show_item("window_notification")

  else:
    dpg.hide_item("window_notification")


def selected(sender, appdata, userdata) -> None:
  """
  SELECT A ROW FROM TABLE
  """

  global row_selected

  if appdata and not(userdata in row_selected): #SELECT
    row_selected = np.append(row_selected, [ int(userdata) ])

  else: #DESELECT
    result = np.where( row_selected == int(userdata) )[0]
    row_selected = np.delete(row_selected, result)

  dpg.set_value("window_main_row_selected", f"Row selected: {len(row_selected)}")


def select_all_rows(sender, appdata) -> None:
  """
  SELECT ALL ROWS FROM TABLE
  """

  global row_selected
  row_selected = np.array( list(range(len(table))), dtype=np.int64)

  for r in row_selected:
    #i = dpg.get_item_children(f"row_{r}", 1)[0]
    dpg.set_value(dpg.get_item_children(f"row_{r}", 1)[0], True)

  dpg.set_value("window_main_row_selected", f"Row selected: {len(row_selected)}")


def deselect_all_rows(sender, appdata) -> None:
  """
  DESSELECT ALL ROWS FROM TABLE
  """
  
  global row_selected
  row_selected = np.array([], dtype=np.int64)

  for r in range(len(table)):
    #i = dpg.get_item_children(f"row_{r}", 1)[0]
    dpg.set_value(dpg.get_item_children(f"row_{r}", 1)[0], False)

  dpg.set_value("window_main_row_selected", f"Row selected: {len(row_selected)}")


def plot_locations(sender, appdata) -> None:
  """
  GET A IMAGE WITH ALL LOCATIONS FROM EVENTS SELECTED
  """
  try:
    if len(row_selected) > 0:
      with plt.ion():
        fig, ax = plt.subplots(figsize=(25, 25), subplot_kw={'projection': ccrs.PlateCarree()}, dpi=100)
        #plt.tight_layout()
        plt.gcf().patch.set_facecolor((0,0,0,0))
        ax.coastlines()
        ax.stock_img()
        ax.set_extent([-180, 180, -90, 90])

        gridlines = ax.gridlines(draw_labels=True, color='gray', alpha=0.5, linestyle='--')
        gridlines.xlocator = plt.FixedLocator(range(-180, 180, 2))
        gridlines.ylocator = plt.FixedLocator(range(-90, 90, 2))
        gridlines.xlabel_style = {'color': 'white'}
        gridlines.ylabel_style = {'color': 'white'}

        #5 latitud
        #6 longitud
        ax.scatter(table[row_selected, 6], table[row_selected, 5], marker='o', edgecolors='black', c="red")

        canvas = FigureCanvas(fig)
        canvas.draw()

        buf = canvas.buffer_rgba()
        image = np.asarray(buf)
        image = image.astype(np.float32) / 255
        plot_locations_texture[:] = image.flatten()

  except Exception as ex:
    notification(msg=ex, title="Error", can_close=True)


def plot_magnitudes(sender, appdata) -> None:
  notification("Wait a second bro...")
  index = np.where(table[:, 9] == appdata)
  rows = table[index][:, [2, 8]]

  mag = rows[:, 1].tolist()
  time = []
  for t in rows[:, 0]:
    time.append(t.timestamp)

  dpg.configure_item("window_plot_magnitudes_points", x=time, y=mag)
  dpg.configure_item("window_plot_magnitudes_lines", x=time, y=mag)
  notification("", show=False)


def save_as_csv(sender, appdata) -> None:
  #try:
  filename = f'{appdata["file_path_name"]}.csv'
  print(filename)

  with open(filename, mode='w') as file:
    csvfile = csv.writer(file, delimiter=';')
    csvfile.writerow(["ID", "Author (by origin)", "Time (UTC)", "Type of event", "Event descriptions", "Latitude", "Longitude", "Depth", "Magnitude", "Type of magnitude"])
    csvfile.writerows(table.tolist())

    #np.savetxt(f"{path}.csv", table, delimiter=", ", fmt="%s",header="ID,Author (by origin),Time (UTC),Type of event,Event descriptions,Latitude,Longitude,Depth,Magnitude,Type of magnitude")

