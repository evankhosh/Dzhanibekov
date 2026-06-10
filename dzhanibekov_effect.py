Web VPython 3.2

scene.title = "Dzhanibekov Effect"
scene.width = 800
scene.height = 600
scene.background = color.black
scene.userzoom = False

metal = vector(0.72, 0.72, 0.75)
_rho           = .001
_r1            = 0.5
_l1            = 3
_r2            = 0.75
_l2            = 5

running = False

def toggle(b):
    global running
    running = not running
    b.text = "Stop" if running else "Start"

scene.append_to_caption("\n")
start_btn = button(text="Start", bind=toggle)

'''
Wingnut Geomtry
'''
wingnut = compound([cylinder(pos=vector(0,0,0), axis=vector(0,1,0),radius=1)]) # arbitrary compound

def create_wingnut(r1, l1, r2, l2):
    parts = []
    
    parts.append(cylinder(
        pos    = vector(0, 0, 0),
        axis   = vector(0, _l1, 0),
        radius = _r1,
        color  = metal
    ))
    
    parts.append(cylinder(
        pos    = vector(-_l2 / 2, 0, 0),
        axis   = vector(_l2, 0, 0),
        radius = _r2,
        color  = metal
    ))
    
    global wingnut
    wingnut.visible = False
    del wingnut
    wingnut = compound(parts, pos=vector(0, 0, 0))

create_wingnut(_r1, _l1, _r2, _l2)

'''
Graphs
'''

g1 = graph(
    title      = "Angular velocity components",
    xtitle     = "time  (s)",
    ytitle     = "ω  (rad/s)",
    width      = 800,
    height     = 300,
    background = color.black,
    foreground = color.white,
    xmin       = 0,  
    xmax       = 20,
    ymin       = -15, 
    ymax       = 15,
    scroll     = True,
    fast       = True
)

curve_wx = gcurve(graph=g1, color=color.red,   label="ω1")
curve_wy = gcurve(graph=g1, color=color.green, label="ω2")
curve_wz = gcurve(graph=g1, color=color.cyan,  label="ω3")

curve_wx.plot(0, 0)
curve_wy.plot(0, 0)
curve_wz.plot(0, 0)

g2 = graph(
    title      = "Euler angles",
    xtitle     = "time (s)",
    ytitle     = "angle (rad)",
    width      = 800,
    height     = 300,
    background = color.black,
    foreground = color.white,
    xmin       = 0,  
    xmax       = 20,
    ymin       = -7, 
    ymax       = 7,
    scroll     = True,
    fast       = True
)

curve_yaw = gcurve(graph=g2, color=color.green,   label="yaw")
curve_pitch  = gcurve(graph=g2, color=color.red, label="pitch")
curve_roll = gcurve(graph=g2, color=color.cyan,  label="roll")

curve_yaw.plot(0, 0)
curve_pitch.plot(0, 0)
curve_roll.plot(0, 0)


g3 = graph(
    title      = "Angular Momentum Components",
    xtitle     = "time (s)",
    ytitle     = "L (kg*m^2/s)",
    width      = 800,
    height     = 300,
    background = color.black,
    foreground = color.white,
    xmin       = 0,      
    xmax       = 20,
    ymin       = -0.005, 
    ymax       = 0.005,
    scroll     = True,
    fast       = True
)

curve_Lx = gcurve(graph=g3, color=color.red,   label="Lx")
curve_Ly = gcurve(graph=g3, color=color.green, label="Ly")
curve_Lz = gcurve(graph=g3, color=color.cyan,  label="Lz")

curve_Lx.plot(0, 0)
curve_Ly.plot(0, 0)
curve_Lz.plot(0, 0)


'''
Principle Axis Arrows
'''

# Principal axes aligned with the body x, y, z axes respectively
principal_axes = [
    vector(1, 0, 0),   # x-axis (red)
    vector(0, 1, 0),   # y-axis (green)
    vector(0, 0, 1)    # z-axis (cyan)
]
scene.append_to_caption("   ")
btn_axes = button(text="Show Principal Axes", bind=toggle_axes)

axis_colors = [color.red, color.green, color.cyan]
axis_scale   = 2.5  

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
            axis   = ev * axis_scale,
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
    wingnut.opacity = 0.5 if axes_visible else 1
    
'''
Physics Engine
'''

def derivs(w, I):
    dw1 = (I.y - I.z) / I.x * w.z * w.y
    dw2 = (I.z - I.x) / I.y * w.z * w.x
    dw3 = (I.x - I.y) / I.z * w.y * w.x
    
    return vector(dw1, dw2, dw3)

def update_euler_angles(euler_angles, w):
    roll, pitch, yaw = euler_angles[0], euler_angles[1], euler_angles[2]

    roll += (w.x + tan(pitch) * (w.y * sin(roll) + w.z * cos(roll))) * dt
    pitch += (w.y * cos(roll) - w.z * sin(roll)) * dt
    yaw += ((w.y * sin(roll) + w.z * cos(roll)) / cos(pitch)) * dt
    
    return [roll, pitch, yaw]
            
def transform(euler_angles):
    roll, pitch, yaw = euler_angles[0], euler_angles[1], euler_angles[2]

    R = [
        [cos(pitch) * cos(yaw), sin(roll) * sin(pitch) * cos(yaw) - cos(roll) * sin(yaw), cos(roll) * sin(pitch) * cos(yaw) + sin(roll) * sin(yaw)],
        [cos(pitch) * sin(yaw), sin(roll) * sin(pitch) * sin(yaw) + cos(roll) * cos(yaw), cos(roll) * sin(pitch) * sin(yaw) - sin(roll) * cos(yaw)],
        [-sin(pitch), sin(roll) * cos(pitch), cos(roll) * cos(pitch)]
    ]

    return R
    
def calculate_com(rho, r1, l1, r2, l2):
    m1 = pi * (r1 ** 2) * l1 * rho
    m2 = pi * (r2 ** 2) * l2 * rho

    return vector(0, (l1 * m1) / (2 * (m1 + m2)), 0)

def moi_cylinder(rho, r, l):
    m = pi * (r ** 2) * l * rho

    parallel = 0.5 * m * (r ** 2)
    perpendicular = 0.25 * m * (r ** 2) + (1 / 12) * m * (l ** 2)

    return [parallel, perpendicular]
def calculate_moi(rho, r1, l1, r2, l2):
    com = calculate_com(rho, r1, l2, r2, l2)

    m1 = pi * (r1 ** 2) * l1 * rho
    m2 = pi * (r2 ** 2) * l2 * rho

    moi1 = moi_cylinder(rho, r1, l1)
    moi2 = moi_cylinder(rho, r2, l2)

    I1 = [moi1[1] + m1 * ((com.y - l1 / 2) ** 2), moi1[0], moi1[1] + m1 * ((com.y - l1 / 2) ** 2)]
    I2 = [moi2[0] + m2 * ((com.y / 2) ** 2), moi2[1], moi2[1] + m2 * ((com.y / 2 ) ** 2)]

    return vector(I1[0] + I2[0], I1[1] + I2[1], I1[2] + I2[2])
    
'''
Initial Conditions

''' 
_w            = vector(0.01, 10, 0)        # iniital ωy and small perturbation ωx
#_I            = vector(1e-4, 3.5e-4, 4e-4) # moments of inertia chosen arbitarily (though they must be distinct)
_I            = calculate_moi(_rho, _r1, _l1, _r2, _l2)
#alert(_I)
dt            = 0.001
t             = 0.0
_euler_angles = [0.0, 0.0, 0.0]
plot_counter  = 0

# modify initial conditions
scene.append_to_caption("   ")
reset_btn = button(text="Reset", bind=reset)
scene.append_to_caption("\n\n")
    
def rotate_about(evt):
    global _w
    if evt.text == 'x':
        _w = vector(10, 0.01, 0)
    elif evt.text == 'y':
        _w = vector(0.01, 10, 0)
    elif evt.text == 'z':
        _w = vector(0, 0.01, 10)

def rotation_buttons():
    if (_I.x > _I.y and _I.x < _I.z or _I.x < _I.y and _I.x > _I.z):
        x_btn = radio(bind=rotate_about, text='x', name='axis', checked=True)
        y_btn = radio(bind=rotate_about, text='y', name='axis')
        z_btn = radio(bind=rotate_about, text='z', name='axis')
        _w = vector(10, 0.01, 0)
    elif (_I.y > _I.x and _I.y < _I.z or _I.y < _I.x and _I.y > _I.z):
        x_btn = radio(bind=rotate_about, text='x', name='axis')
        y_btn = radio(bind=rotate_about, text='y', name='axis', checked=True)
        z_btn = radio(bind=rotate_about, text='z', name='axis')
        _w = vector(0.01, 10, 0)
    else:
        x_btn = radio(bind=rotate_about, text='x', name='axis')
        y_btn = radio(bind=rotate_about, text='y', name='axis')
        z_btn = radio(bind=rotate_about, text='z', name='axis', checked=True)
        _w = vector(0, 0.01, 10)

scene.append_to_caption("\n\nChoose the axis to rotate about:")
rotation_buttons()
    
def set_cylinder_len(evt):
    if evt.id is 'l1':
        global _l1
        _l1 = evt.value
    elif evt.id is 'l2':
        global _l2
        _l2 = evt.value
        
    create_wingnut(_r1, _l1, _r2, _l2)
    global _I
    _I = calculate_moi(_rho, _r1, _l1, _r2, _l2)

scene.append_to_caption("\n\n")
scene.append_to_caption("Cylinder 1 Length:")    
l1_slider = slider(bind=set_cylinder_len, min=2, max=10, step=0.1, value=_l1, id='l1')
scene.append_to_caption("\n\n")
scene.append_to_caption("Cylinder 2 Length:")
l2_slider = slider(bind=set_cylinder_len, min=2, max=10, step=0.1, value=_l2, id='l2')

def set_omega(evt):
    global _w
    if evt.id is 'w':
        _w = evt.value

scene.append_to_caption("\n\n")
scene.append_to_caption("Initial Angular Velocity:")
l2_slider = slider(bind=set_omega, min=5, max=1000, step=5, value=_w, id='w')

def reset():
    global running, wingnut, _w, _I, dt, t, _euler_angles, plot_counter, \
           _r1, _l1, _r2, _l2, \
           l1_slider, l2_slider, \
           curve_wx, curve_wy, curve_wz, \
           curve_yaw, curve_pitch, curve_roll, \
           curve_Lx, curve_Ly, curve_Lx, \
           x_btn, y_btn, z_btn
       
    start_btn.text = "Start"
    running = False
    
    R = transform([0, 0, 0])
    wingnut.axis = vector(R[0][0], R[1][0], R[2][0])
    wingnut.up   = vector(R[0][1], R[1][1], R[2][1])
    
    for i in range(len(principal_arrows)):
        principal_arrows[i].axis = vector(R[0][i], R[1][i], R[2][i]) * axis_scale
           
    _w            = vector(0.01, 10, 0)
#    _I            = vector(1e-4, 3.5e-4, 4e-4)
    _I            = calculate_moi(rho, r1, l1, r2, l2)
    dt            = 0.001
    t             = 0.0
    _euler_angles = [0.0, 0.0, 0.0]
    plot_counter  = 0
    
    _r1            = 0.5
    _l1            = 3
    _r2            = 0.75
    _l2            = 5
    
    l1_slider.delete()
    l2_slider.delete()
    l1_slider = slider(bind=set_cylinder_len, min=2, max=10, step=0.1, value=_l1, id='l1')
    l2_slider = slider(bind=set_cylinder_len, min=2, max=10, step=0.1, value=_l2, id='l2')
    
    curve_wx.delete()
    curve_wy.delete()
    curve_wz.delete()
    g1.xmin = 0
    g1.xmax = 20
    curve_yaw.delete()
    curve_pitch.delete()
    curve_roll.delete()
    g2.xmin = 0
    g2.xmax = 20
    curve_Lx.delete()
    curve_Ly.delete()
    curve_Lz.delete()
    g3.xmin = 0
    g3.xmax = 20
    
    x_btn.delete()
    y_btn.delete()
    z_btn.delete()
    rotation_buttons()

    
'''
Animation
'''

draw_principal_axes()

while True:
    rate(1/dt)
    
    if not running:
        continue
        
    # update ω
    _w += derivs(_w, _I) * dt
    
    # update euler angles
    _euler_angles = update_euler_angles(_euler_angles, _w)
    for i in range(3):
        if _euler_angles[i] > 2 * pi:
            _euler_angles[i] = _euler_angles[i] % (2 * pi)
        if _euler_angles[i] < 2 * pi:
            _euler_angles[i] = _euler_angles[i] % (-2 * pi)
    
    # update wingnut orientation
    R = transform(_euler_angles)
    wingnut.axis = vector(R[0][0], R[1][0], R[2][0])
    wingnut.up   = vector(R[0][1], R[1][1], R[2][1])
    
    for i in range(len(principal_arrows)):
        principal_arrows[i].axis = vector(R[0][i], R[1][i], R[2][i]) * axis_scale
    
    # we plot to graphs every 5 steps
    plot_counter += 1
    if plot_counter % 5 == 0:
        curve_wx.plot(t, _w.x)
        curve_wy.plot(t, _w.y)
        curve_wz.plot(t, _w.z)
        
        curve_roll.plot(t, _euler_angles[0])
        curve_pitch.plot(t, _euler_angles[1])
        curve_yaw.plot(t, _euler_angles[2])
        
        L_body = vector(_I.x * _w.x, _I.y * _w.y, _I.z * _w.z)
        Lx = dot(vector(R[0][0], R[0][1], R[0][2]), L_body)
        Ly = dot(vector(R[1][0], R[1][1], R[1][2]), L_body)
        Lz = dot(vector(R[2][0], R[2][1], R[2][2]), L_body)
        
        curve_Lx.plot(t, Lx)
        curve_Ly.plot(t, Ly)
        curve_Lz.plot(t, Lz)
    
    t += dt
