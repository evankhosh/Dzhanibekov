Web VPython 3.2

scene.title = "Wing Nut"
scene.width = 800
scene.height = 600
scene.background = color.black
scene.camera.pos = vector(3, 2.5, 5)
scene.camera.axis = vector(-3, -2.5, -5)

metal = vector(0.72, 0.72, 0.75)
dark  = vector(0.20, 0.20, 0.22)

# Central cylindrical body 
cylinder(
    pos    = vector(0, -0.3, 0),
    axis   = vector(0, 3, 0),
    radius = 0.55,
    color  = metal
)

# Threaded hole through center
cylinder(
    pos    = vector(0, -0.31, 0),
    axis   = vector(0, 0.62, 0),
    radius = 0.22,
    color  = dark
)

# Two wings
for side in [-1, 1]:
    # Main wing slab
    box(
        pos   = vector(side * 1.05, 0, 0),
        size  = vector(1.0, 0.55, 0.30),
        color = metal
    )
    # Narrow tip slab
    box(
        pos   = vector(side * 1.62, 0, 0),
        size  = vector(0.22, 0.50, 0.22),
        color = metal
    )
    # Rounded tip
    sphere(
        pos    = vector(side * 1.74, 0, 0),
        radius = 0.13,
        color  = metal
    )

gd = graph(
    title  = "Angular velocity components",
    xtitle = "time  (s)",
    ytitle = "ω  (rad/s)",
    width  = 800,
    height = 300,
    background = color.black,
    foreground = color.white,
    xmin = 0,  xmax = 20,
    ymin = -8, ymax = 8,
    fast   = True
)
 
curve_wx = gcurve(graph=gd, color=color.red,   label="ωx  (stable 1)")
curve_wy = gcurve(graph=gd, color=color.green, label="ωy  (stable 2)")
curve_wz = gcurve(graph=gd, color=color.cyan,  label="ωz  (intermediate)")
 
curve_wx.plot(0, 0)
curve_wy.plot(0, 0)
curve_wz.plot(0, 0)
