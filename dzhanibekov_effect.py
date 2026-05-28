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

g1 = graph(
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
 
curve_wx = gcurve(graph=g1, color=color.red,   label="ωx")
curve_wy = gcurve(graph=g1, color=color.green, label="ωy")
curve_wz = gcurve(graph=g1, color=color.cyan,  label="ωz")
 
curve_wx.plot(0, 0)
curve_wy.plot(0, 0)
curve_wz.plot(0, 0)

g2 = graph(
    title  = "Euler angles",
    xtitle = "time  (s)",
    ytitle = "angle (rad)",
    width  = 800,
    height = 300,
    background = color.black,
    foreground = color.white,
    xmin = 0,  xmax = 20,
    ymin = -8, ymax = 8,
    fast   = True
)
 
curve_alpha = gcurve(graph=g2, color=color.red,   label="alpha")
curve_beta = gcurve(graph=g2, color=color.green, label="beta")
curve_gamma = gcurve(graph=g2, color=color.cyan,  label="gamma")
 
curve_alpha.plot(0, 0)
curve_beta.plot(0, 0)
curve_gamma.plot(0, 0)

g3 = graph(
    title  = "Moment of Inertia Components",
    xtitle = "time  (s)",
    ytitle = "moment of inertia (kg * m^2)",
    width  = 800,
    height = 300,
    background = color.black,
    foreground = color.white,
    xmin = 0,  xmax = 20,
    ymin = -8, ymax = 8,
    fast   = True
)
 
curve_ix = gcurve(graph=g3, color=color.red,   label="Ix")
curve_iy = gcurve(graph=g3, color=color.green, label="Iy")
curve_iz = gcurve(graph=g3, color=color.cyan,  label="Iz")
 
curve_ix.plot(0, 0)
curve_iy.plot(0, 0)
curve_iz.plot(0, 0)
