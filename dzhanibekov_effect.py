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
 
# Principal moments of inertia (kg·m²)
# Derived analytically from geometry: scale 1 unit = 0.03 m, rho_steel = 7800 kg/m³
# Parallel-axis theorem applied to each primitive about the global CoM
I1 = 1.91e-4   # smallest     — stable spin axis (body y)
I2 = 5.22e-4   # intermediate — UNSTABLE spin axis (body x)
I3 = 6.31e-4   # largest      — stable spin axis (body z)
 
 
def derivs(omega):
    w1, w2, w3 = omega[0], omega[1], omega[2]
    dw1 = (I2 - I3) / I1 * w2 * w3
    dw2 = (I3 - I1) / I2 * w3 * w1
    dw3 = (I1 - I2) / I3 * w1 * w2
    return [dw1, dw2, dw3]
 
 
def rk4_omega(omega, dt):
    k1 = derivs(omega)
    omega_k2 = [omega[j] + 0.5 * dt * k1[j] for j in range(3)]
    k2 = derivs(omega_k2)
    omega_k3 = [omega[j] + 0.5 * dt * k2[j] for j in range(3)]
    k3 = derivs(omega_k3)
    omega_k4 = [omega[j] + dt * k3[j] for j in range(3)]
    k4 = derivs(omega_k4)
    return [omega[j] + (dt / 6.0) * (k1[j] + 2*k2[j] + 2*k3[j] + k4[j])
            for j in range(3)]
 
 
# Small ω1 perturbation seeds the instability; ω2 is the main spin
omega = [0.01, 5.0, 0.0]   # [ω1, ω2, ω3]  rad/s
 
dt           = 0.001   # timestep (s)
t            = 0.0     # simulation clock (s)
plot_counter = 0       # throttle graph updates to every 5 physics steps
 
 
while True:
    rate(1000)
 
    omega = rk4_omega(omega, dt)
 
    plot_counter += 1
    if plot_counter % 5 == 0:
        curve_wx.plot(t, omega[0])   # ω1 — body axis 1 (y)
        curve_wy.plot(t, omega[1])   # ω2 — body axis 2 (x), main spin
        curve_wz.plot(t, omega[2])   # ω3 — body axis 3 (z)
 
    t += dt
