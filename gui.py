from riverdi.displays.bt81x import ctp50
from bridgetek.bt81x import bt81x

palette_default = bt81x.Palette((0xff, 0xff, 0xff), (0, 0, 0xff))
palette_pressed = bt81x.Palette((0xff, 0xff, 0xff), (0xff, 0, 0))


#
# loadImage
#
def loadImage(image):
    bt81x.load_image(0, 0, image)


#
# showLogo
#
def showLogo():

    # start
    bt81x.dl_start()
    bt81x.clear_color(rgb=(0xff, 0xff, 0xff))
    bt81x.clear(1, 1, 1)

    # image
    image = bt81x.Bitmap(1, 0, (bt81x.ARGB4, 642 * 2), (bt81x.BILINEAR, bt81x.BORDER, bt81x.BORDER, 642, 144))
    image.prepare_draw()
    image.draw(((bt81x.display_conf.width - 642)//2, (bt81x.display_conf.height - 144)//2), vertex_fmt=0)

    # display
    bt81x.display()
    bt81x.swap_and_empty()


#
# showSpinner
#
def showSpinner(msg):

    # start
    bt81x.dl_start()
    bt81x.clear(1, 1, 1)

    # text
    txt = bt81x.Text(400, 350, 30, bt81x.OPT_CENTERX | bt81x.OPT_CENTERY, msg, )
    bt81x.add_text(txt)

    # spinner
    bt81x.spinner(400, 240, bt81x.SPINNER_CIRCLE, 0)

    # display
    bt81x.display()
    bt81x.swap_and_empty()

    # wait a second - just to improve UI experience ;)
    sleep(1000)


#
# showSpinner
#
def showMenuBar(position):

    # start
    bt81x.dl_start()
    bt81x.clear(1, 1, 1)

    btn = bt81x.Button(0, 384, 268, 96, 31, bt81x.OPT_FLAT, "Sensors",)
    btn.palette = palette_pressed if position==1 else palette_default
    bt81x.track (0, 384, 268, 96, 1)
    bt81x.tag(1)
    bt81x.add_button(btn)
    
    btn = bt81x.Button(266, 384, 268, 96, 31, bt81x.OPT_FLAT, "Statistics",)
    btn.palette = palette_pressed if position==2 else palette_default
    bt81x.track (266, 384, 268, 96, 2)
    bt81x.tag(2)
    bt81x.add_button(btn)
    
    btn = bt81x.Button(532, 384, 266, 96, 31, bt81x.OPT_FLAT, "Processes",)
    btn.palette = palette_pressed if position==3 else palette_default
    bt81x.track (532, 384, 266, 96, 3)
    bt81x.tag(3)
    bt81x.add_button(btn)


#
# showSensorsScreen
#
def showSensorsScreen(rpi_temp_1, rpi_temp_2, rpi_temp_3, rpi_temp_4):

    # menuBar
    showMenuBar(1)

    # title
    txt = bt81x.Text(400, 55, 31, bt81x.OPT_CENTERX | bt81x.OPT_CENTERY, "Temperature Sensors", )
    bt81x.add_text(txt)

    txt.options = bt81x.OPT_CENTERX | bt81x.OPT_CENTERY;
    txt.font = 29;

    txt.text = "Living Room:"
    txt.x = 220;
    txt.y = 130;
    bt81x.add_text(txt)

    txt.text = "Bedroom:"
    txt.x = 580;
    txt.y = 130;
    bt81x.add_text(txt)

    txt.text = "Kitchen:"
    txt.x = 220;
    txt.y = 250;
    bt81x.add_text(txt)

    txt.text = "Bathroom:"
    txt.x = 580;
    txt.y = 250;
    bt81x.add_text(txt)

    ###

    txt.options = bt81x.OPT_CENTERX | bt81x.OPT_CENTERY;
    txt.font = 31;

    txt.text = "%.1f" % rpi_temp_1 + " deg"
    txt.x = 220;
    txt.y = 180;
    bt81x.add_text(txt)

    txt.text = "%.1f" % rpi_temp_2 + " deg"
    txt.x = 580;
    txt.y = 180;
    bt81x.add_text(txt)

    txt.text = "%.1f" % rpi_temp_3 + " deg"
    txt.x = 220;
    txt.y = 300;
    bt81x.add_text(txt)

    txt.text = "%.1f" % rpi_temp_4 + " deg"
    txt.x = 580;
    txt.y = 300;
    bt81x.add_text(txt)

    bt81x.display()
    bt81x.swap_and_empty()


#
# showStatisticsScreen()
#
def showStatisticsScreen(cpu_load_cur, cpu_temp_main, mem_info_free, mem_swap_free):
    
    # menuBar
    showMenuBar(2)

    # title
    txt = bt81x.Text(400, 55, 31, bt81x.OPT_CENTERX | bt81x.OPT_CENTERY, "Device Status", )
    bt81x.add_text(txt)

    txt.options = bt81x.OPT_CENTERX | bt81x.OPT_CENTERY;
    txt.font = 29;

    txt.text = "CPU Utilization:"
    txt.x = 220;
    txt.y = 130;
    bt81x.add_text(txt)

    txt.text = "CPU Temperature:"
    txt.x = 580;
    txt.y = 130;
    bt81x.add_text(txt)

    txt.text = "Memory Free:"
    txt.x = 220;
    txt.y = 250;
    bt81x.add_text(txt)

    txt.text = "Swap Free:"
    txt.x = 580;
    txt.y = 250;
    bt81x.add_text(txt)

    ###

    txt.options = bt81x.OPT_CENTERX | bt81x.OPT_CENTERY;
    txt.font = 31;

    txt.text = "%.1f" % cpu_load_cur + "%"
    txt.x = 220;
    txt.y = 180;
    bt81x.add_text(txt)

    txt.text = "%.1f" % cpu_temp_main + " deg"
    txt.x = 580;
    txt.y = 180;
    bt81x.add_text(txt)

    txt.text = str(mem_info_free) + " MB"
    txt.x = 220;
    txt.y = 300;
    bt81x.add_text(txt)

    txt.text = str(mem_swap_free) + " MB"
    txt.x = 580;
    txt.y = 300;
    bt81x.add_text(txt)

    bt81x.display()
    bt81x.swap_and_empty()


#
# showProcessMonitor
#
def showProcessMonitor(rpi_top_proc_1,rpi_top_proc_2,rpi_top_proc_3,rpi_top_proc_4):

    # menuBar
    showMenuBar(3)

    # title
    txt = bt81x.Text(400, 55, 31, bt81x.OPT_CENTERX | bt81x.OPT_CENTERY, "Process Monitor", )
    bt81x.add_text(txt)

    txt.options = bt81x.OPT_CENTERY;

    ### 1 ###
    
    data = rpi_top_proc_1.split("|")

    txt.text = data[0]
    txt.x = 50;
    txt.y = 115;
    txt.font = 29;
    bt81x.add_text(txt)
    
    txt.text = "PID: " + data[1]
    txt.x = 50;
    txt.y = 145;
    txt.font = 27;
    bt81x.add_text(txt)
    
    txt.text = "Memory usage: " + data[2]
    txt.x = 200;
    txt.y = 145;
    txt.font = 27;
    bt81x.add_text(txt)
    
    ### 2 ###
    
    data = rpi_top_proc_2.split("|")

    txt.text = data[0]
    txt.x = 50;
    txt.y = 185;
    txt.font = 29;
    bt81x.add_text(txt)
    
    txt.text = "PID: " + data[1]
    txt.x = 50;
    txt.y = 215;
    txt.font = 27;
    bt81x.add_text(txt)
    
    txt.text = "Memory usage: " + data[2]
    txt.x = 200;
    txt.y = 215;
    txt.font = 27;
    bt81x.add_text(txt)
    
    ### 3 ###
    
    data = rpi_top_proc_3.split("|")

    txt.text = data[0]
    txt.x = 50;
    txt.y = 255;
    txt.font = 29;
    bt81x.add_text(txt)
    
    txt.text = "PID: " + data[1]
    txt.x = 50;
    txt.y = 285;
    txt.font = 27;
    bt81x.add_text(txt)
    
    txt.text = "Memory usage: " + data[2]
    txt.x = 200;
    txt.y = 285;
    txt.font = 27;
    bt81x.add_text(txt)
    
    ### 4 ###
    
    data = rpi_top_proc_4.split("|")

    txt.text = data[0]
    txt.x = 50;
    txt.y = 325;
    txt.font = 29;
    bt81x.add_text(txt)
    
    txt.text = "PID: " + data[1]
    txt.x = 50;
    txt.y = 355;
    txt.font = 27;
    bt81x.add_text(txt)
    
    txt.text = "Memory usage: " + data[2]
    txt.x = 200;
    txt.y = 355;
    txt.font = 27;
    bt81x.add_text(txt)
    
    bt81x.display()
    bt81x.swap_and_empty()