"""
Made by Mido.dev
Support me: https://github.com/MidoDev993

a simple earthquake viewer with dearpygui
"""

import dearpygui.dearpygui as dpg
import functions
from datetime import datetime

dpg.create_context()


#NOTIFICATION WINDOW*
with dpg.window(modal=True, show=False, width=375, height=100, no_close=True, tag="window_notification", label="", horizontal_scrollbar=True):
    dpg.add_text(default_value="", tag="window_notification_label")


#SEARCH WINDOW*
with dpg.window(label="Search", show=False, tag="window_search", width=625, height=800, horizontal_scrollbar=True):
    items = {}

    #START TIME
    dpg.add_text(default_value="Start time (UTC):*")
    with dpg.group(horizontal=True):
        items["starttime.year"] = dpg.add_input_int(default_value=datetime.now().year-1,  width=100, label=":Year  ")
        items["starttime.month"] = dpg.add_input_int(default_value=1,  width=100, label=":Month  ")
        items["starttime.day"] = dpg.add_input_int(default_value=1,  width=100, label=":Day  ")
        items["starttime.time"] = dpg.add_time_picker(hour24=True, default_value={'sec': 0, 'min': 0, 'hour': 0})
    dpg.add_spacer(height=25)

    #END TIME
    dpg.add_text(default_value="End time (UTC):*")
    with dpg.group(horizontal=True):
        items["endtime.year"] = dpg.add_input_int(default_value=datetime.now().year,  width=100, label=":Year  ")
        items["endtime.month"] = dpg.add_input_int(default_value=1,  width=100, label=":Month  ")
        items["endtime.day"] = dpg.add_input_int(default_value=1,  width=100, label=":Day  ")
        items["endtime.time"] = dpg.add_time_picker(hour24=True, default_value={'sec': 0, 'min': 0, 'hour': 0})
    dpg.add_spacer(height=25)

    #Minimum magnitude
    items["minmagnitude"] = dpg.add_input_float(min_clamped=True, min_value=0, width=200, label=":Minimum magnitude")
    with dpg.tooltip(parent=items["minmagnitude"]):
        dpg.add_text(default_value="Limit to events with a magnitude larger than the specified minimum.")
    dpg.add_spacer(height=25)

    #Maximum magnitude
    items["maxmagnitude"] = dpg.add_input_float(min_clamped=True, min_value=0, width=200, label=":Maximum magnitude")
    with dpg.tooltip(parent=items["maxmagnitude"]):
        dpg.add_text(default_value="Limit to events with a magnitude smaller than the specified maximum.")
    dpg.add_spacer(height=25)

    #Latitude
    items["latitude"] = dpg.add_input_float(width=200, label=":Latitude")
    with dpg.tooltip(parent=items["latitude"]):
        dpg.add_text(default_value="Specify the latitude to be used for a radius search.")
    dpg.add_spacer(height=25)

    #Longitude
    items["longitude"] = dpg.add_input_float(width=200, label=":Longitude")
    with dpg.tooltip(parent=items["longitude"]):
        dpg.add_text(default_value="Specify the longitude to be used for a radius search.")
    dpg.add_spacer(height=25)

    #Minimum radius
    items["minradius"] = dpg.add_input_float(min_clamped=True, min_value=0, width=200, label=": Minimum radius")
    with dpg.tooltip(parent=items["minradius"]):
        dpg.add_text(default_value="Limit to events within the specified minimum number of degrees from the geographic point defined by the latitude and longitude parameters.")
    dpg.add_spacer(height=25)

    #Maximum radius
    items["maxradius"] = dpg.add_input_float(min_clamped=True, min_value=0, width=200, label=":Maximum radius")
    with dpg.tooltip(parent=items["maxradius"]):
        dpg.add_text(default_value="Limit to events within the specified maximum number of degrees from the geographic point defined by the latitude and longitude parameters.")
    dpg.add_spacer(height=25)

    #Minimum depth (in km
    items["mindepth"] = dpg.add_input_float(min_clamped=True, min_value=0, width=200, label=":Minimum depth (in km)")
    with dpg.tooltip(parent=items["mindepth"]):
        dpg.add_text(default_value="Limit to events with depth, in kilometers, larger than the specified minimum.")
    dpg.add_spacer(height=25)

    #Maximum depth (in km)
    items["maxdepth"] = dpg.add_input_float(min_clamped=True, min_value=0, width=200, label=":Maximum depth (in km)")
    with dpg.tooltip(parent=items["maxdepth"]):
        dpg.add_text(default_value="Limit to events with depth, in kilometers, smaller than the specified maximum.")
    dpg.add_spacer(height=25)

    #Limit
    items["limit"] = dpg.add_input_int(min_clamped=True,min_value=0, width=200, label=":Limit")
    with dpg.tooltip(parent=items["limit"]):
        dpg.add_text(default_value="Limit the results to the specified number of events.")
    dpg.add_spacer(height=25)

    #Order by
    items["orderby"] = dpg.add_combo(items=[None, "time", "time-asc", "magnitude", "magnitude-asc"], default_value=None, width=200, label=":Order by")
    with dpg.tooltip(parent=items["orderby"]):
        dpg.add_text(default_value="""-time: order by origin descending time
-time-asc: order by origin ascending time
-magnitude: order by descending magnitude
-magnitude-asc: order by ascending magnitude""")

    dpg.add_spacer(height=50)
    dpg.add_button(label="Start search", callback=functions.search, user_data=items)    


#PLOT WINDOW*
with dpg.window(label="Plots", tag="window_plot", width=400, height=400, horizontal_scrollbar=True, show=False):
    with dpg.tab_bar():

        with dpg.tab(label="Locations"):
            dpg.add_button(label="Show locations", callback=functions.plot_locations)

            with dpg.texture_registry(show=False):
                dpg.add_raw_texture(width=2500, height=2500, default_value=functions.plot_locations_texture, tag="window_plot_locations_texture")

            with dpg.plot(height=-1, width=-1, no_mouse_pos=True):
                dpg.add_plot_axis(axis=dpg.mvXAxis, no_gridlines=True, no_tick_labels=True)
                dpg.add_plot_axis(axis=dpg.mvYAxis, tag="window_plot_locations_axis_y", no_gridlines=True, no_tick_labels=True)
                dpg.add_image_series(texture_tag="window_plot_locations_texture", bounds_min=[0, 0], bounds_max=[2500, 2500], parent="window_plot_locations_axis_y")


        with dpg.tab(label="Magnitudes"):
            dpg.add_combo([], tag="window_plot_magnitudes_selector", callback=functions.plot_magnitudes)

            with dpg.plot(height=-1, width=-1, use_ISO8601=True, use_24hour_clock=True, query=True):
                dpg.add_plot_axis(axis=dpg.mvXAxis, label="Date time (UTC)", scale=dpg.mvPlotScale_Time)
                dpg.add_plot_axis(axis=dpg.mvYAxis, label="Magnitude", tag="window_plot_magnitudes_axis_y")

                dpg.add_scatter_series(x=[], y=[], tag="window_plot_magnitudes_points", parent="window_plot_magnitudes_axis_y")
                dpg.add_line_series(x=[], y=[], tag="window_plot_magnitudes_lines", parent="window_plot_magnitudes_axis_y")


#WINDOW MAIN
with dpg.window(tag="window_main"):

    with dpg.menu_bar():
        dpg.add_button(label="Menu search", callback=lambda sender, appdata: dpg.show_item("window_search"))
        dpg.add_spacer(width=5)
        
        dpg.add_button(label="Show plot", callback=lambda sender, appdata: dpg.show_item("window_plot"))
        dpg.add_spacer(width=5)

        dpg.add_file_dialog(label="Export as csv", callback=functions.save_as_csv, show=False, modal=True, tag="window_main_filedialog_csv")
        dpg.add_button(label="Export as csv", callback=lambda sender, appdata: dpg.show_item("window_main_filedialog_csv"))


    with dpg.child_window(horizontal_scrollbar=True):
        dpg.add_input_float(label=":Font scale", width=200, default_value=1.0, min_value=0.5, max_value=2, min_clamped=True, max_clamped=True, callback=lambda sender, appdata: dpg.set_global_font_scale(appdata))

        with dpg.group(horizontal=True):
            dpg.add_button(label="Select all", callback=functions.select_all_rows)
            dpg.add_button(label="Deselect all", callback=functions.deselect_all_rows)
            dpg.add_text(default_value="Row selected: 0", tag="window_main_row_selected")

        with dpg.table(header_row=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True, resizable=True, clipper=True, tag="window_main_table_info"):
            dpg.add_table_column(label="ID")
            dpg.add_table_column(label="Author (by origin)")
            dpg.add_table_column(label="Time (UTC)")
            dpg.add_table_column(label="Type of event")
            dpg.add_table_column(label="Event descriptions")
            dpg.add_table_column(label="Latitude")
            dpg.add_table_column(label="Longitude")
            dpg.add_table_column(label="Depth")
            dpg.add_table_column(label="Magnitude")
            dpg.add_table_column(label="Type of magnitude")


dpg.create_viewport(title='Earthquake viewer 1.0.0', width=1200, height=950)
dpg.set_primary_window("window_main", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
print("DONE")