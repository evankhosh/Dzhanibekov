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

I1 = 1.91e-4   # smallest     — stable spin axis
I2 = 5.22e-4   # intermediate — UNSTABLE spin axis
I3 = 6.31e-4   # largest      — stable spin axis

principal_axes = [
    [1.0, 0.0, 0.0],   # I1 → x-axis (red)
    [0.0, 1.0, 0.0],   # I2 → y-axis (green)
    [0.0, 0.0, 1.0]    # I3 → z-axis (cyan)
]

scene.append_to_caption("   ")                      # spacer
btn_axes = button(text="Show Principal Axes", bind=toggle_axes)
scene.append_to_caption("\n\n")

axis_colors = [color.red, color.green, color.cyan]
axis_labels  = ["I1", "I2", "I3"]
axis_scale   = 2.5   # display length (m) — tune to taste

principal_arrows = []

def draw_principal_axes():
    global principal_arrows
    # Remove old arrows if they exist
    for arr in principal_arrows:
        arr.visible = False
    principal_arrows = []

    for k in range(3):
        ev = principal_axes[k]
        arr = arrow(
            pos    = vector(0, 0, 0),
            axis   = vector(ev[0], ev[1], ev[2]) * axis_scale,
            color  = axis_colors[k],
            shaftwidth = 0.06,
            headwidth  = 0.14,
            headlength = 0.18,
            visible    = False          # hidden until user clicks Show
        )
        principal_arrows.append(arr)


axes_visible = False

def toggle_axes(b):
    global axes_visible
    axes_visible = not axes_visible
    for arr in principal_arrows:
        arr.visible = axes_visible
    b.text = "Hide Principal Axes" if axes_visible else "Show Principal Axes"

def euler_angles(euler_angles, omega)
    alpha, beta, gamma = euler_angles[0], euler_angles[1], euler_angles[2]
    w1, w2, w3 = omega[0], omega[1], omega[2]
    
    beta = alpha + (w1 * np.sin(gamma) + w2 * np.cos(gamma))/np.sin(beta) * dt
    beta = beta + (w1 * np.cos(gamma) - w2 * np.sin(gamma)) * dt
    gamma = gamma + (w3 - (w1 * np.sin(gamma) + w2 * np.cos(gamma))/np.sin(beta) * np.cos(beta)) * dt
    
    return [alpha, beta, gamma]
    
def transform(euler_angles)
    alpha, beta, gamma = euler_angles[0], euler_angles[1], euler_angles[2]
    
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(alpha), -np.sin(alpha)],
        [0, np.sin(alpha), np.cos(alpha)]
        ])
    
    Ry = np.array([
        [np.cos(beta), 0, np.sin(beta)],
        [0, 1, 0],
        [-np.sin(beta), 0, np.cos(beta)]
        ])
        
    Rz = np.array([
        [np.cos(gamma), -np.sin(gamma), 0],
        [np.sin(gamma), np.cos(gamma), 0],
        [0, 0, 1]
        ])
        
    return Rx @ Ry @ Rz

omega        = [0.01, 5.0, 0.0]
q            = [1.0, 0.0, 0.0, 0.0]

dt           = 0.001
t            = 0.0
plot_counter = 0

draw_principal_axes()

while True:
    rate(1000)

    if not running:
        continue

    # Evolve angular velocity (body frame)
    

    # Evolve euler angles
    euler_angles = euler_angles(euler_angles)

    # Apply orientation to the compound object
    wingnut.axis = transform(euler_angles) * wingnut.axis
    # wingnut.up   = vector(R[0][1], R[1][1], R[2][1])

    # Plot to graphs every 5 steps
    plot_counter += 1
    if plot_counter % 5 == 0:
        Lb = [I1*omega[0], I2*omega[1], I3*omega[2]]
        Lx = R[0][0]*Lb[0] + R[0][1]*Lb[1] + R[0][2]*Lb[2]
        Ly = R[1][0]*Lb[0] + R[1][1]*Lb[1] + R[1][2]*Lb[2]
        Lz = R[2][0]*Lb[0] + R[2][1]*Lb[1] + R[2][2]*Lb[2]

        curve_wx.plot(t, omega[0])
        curve_wy.plot(t, omega[1])
        curve_wz.plot(t, omega[2])

        curve_alpha.plot(t, euler_angles[0])
        curve_beta.plot(t,  euler_angles[1])
        curve_gamma.plot(t, euler_angles[2])

        curve_Lx.plot(t, Lx)
        curve_Ly.plot(t, Ly)
        curve_Lz.plot(t, Lz)

    t += dt
