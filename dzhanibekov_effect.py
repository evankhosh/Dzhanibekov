Web VPython 3.2

scene.title = "Dzhanibekov Effect"
scene.width = 800
scene.height = 600
scene.background = color.black

metal = vector(0.72, 0.72, 0.75)

running = False

def toggle(b):
    global running
    running = not running
    b.text = "Stop" if running else "Start"

scene.append_to_caption("\n")
btn = button(text="Start", bind=toggle)

'''
Wingnut Geomtry
'''

parts = []

parts.append(cylinder(
    pos    = vector(0, -.5, 0),
    axis   = vector(0, 3, 0),
    radius = 0.5,
    color = metal
))

parts.append(cylinder(
    pos    = vector(-2.5, -.5, 0),
    axis   = vector(5, 0, 0),
    radius = 0.75,
    color = metal
))

wingnut = compound(parts, pos=vector(0, 0, 0))


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
scene.append_to_caption("\n\n")

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

#    roll  += (w.x * cos(yaw) / cos(pitch) - w.y * sin(yaw) / cos(pitch)) * dt
#    pitch += (w.x * sin(yaw) + w.y * cos(yaw)) * dt
#    yaw   += (-w.x * cos(yaw) * sin(pitch) / cos(pitch) + w.y * sin(pitch) * sin(yaw) / cos(pitch) + w.z) * dt
    
    return [roll, pitch, yaw]

def rot_90_cw(m): # helper for mat_mul_3x3()
    # copy m to res
    res = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    for i in range(3):
        for j in range(3):
            res[i][j] = m[i][j]
            
    # transpose
    for i in range(3):
        for j in range(3):
            res[i][j] = m[j][i]
    
    # reflect
    for i in range(3):
        temp = res[i][0]
        res[i][0] = res[i][2]
        res[i][2] = temp
    
    return res
    
def mat_mul_3x3(m1, m2): # we are using this only to multiply the rotation matrices
    res = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    
    m2 = rot_90_cw(m2)
    
    for i in range(3):
        for j in range(3):
            res[i][j] = dot(vector(m1[i][0], m1[i][1], m1[i][2]), vector(m2[j][0], m2[j][1], m2[j][2]))
    
    return res
    
def mat_mul(A, B):
    rows = len(A)
    cols = len(B[0])
    result = [[0] * cols for i in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
 
    return result
            
def transform(euler_angles):
    roll, pitch, yaw = euler_angles[0], euler_angles[1], euler_angles[2]
    
#    R = [
#        [cos(pitch) * cos(yaw), -cos(pitch) * sin(yaw), sin(pitch)],
#        [cos(roll) * sin(yaw) + cos(yaw) * sin(roll) * sin(pitch), cos(roll) * cos(yaw) - sin(roll) * sin(pitch) * sin(yaw), -cos(pitch) * sin(roll)],
#        [sin(roll) * sin(yaw) - cos(roll) * cos(yaw) * sin(pitch), cos(yaw) * sin(roll) + cos(roll) * sin(pitch) * sin(yaw), cos(roll) * cos(pitch)]
#    ]

    R = [
        [cos(pitch) * cos(yaw), sin(roll) * sin(pitch) * cos(yaw) - cos(roll) * sin(yaw), cos(roll) * sin(pitch) * cos(yaw) + sin(roll) * sin(yaw)],
        [cos(pitch) * sin(yaw), sin(roll) * sin(pitch) * sin(yaw) + cos(roll) * cos(yaw), cos(roll) * sin(pitch) * sin(yaw) - sin(roll) * cos(yaw)],
        [-sin(pitch), sin(roll) * cos(pitch), cos(roll) * cos(pitch)]
    ]

    return R
    
#    Rx = [
#        [1, 0, 0],
#        [0, cos(roll), -sin(roll)],
#        [0, sin(roll), cos(roll)]
#    ]
#    
#    Ry = [
#        [cos(pitch), 0, sin(pitch)],
#        [0, 1, 0],
#        [-sin(pitch), 0, cos(pitch)]
#    ]
#        
#    Rz = [
#        [cos(yaw), -sin(yaw), 0],
#        [sin(yaw), cos(yaw), 0],
#        [0, 0, 1]
#    ]
#        
#    return mat_mul(mat_mul(Rx, Ry), Rz)
    
'''
Initial Conditions

''' 
_w           = vector(0.01, 10, 0)         # iniital ωy and small perturbation ωx
_I           = vector(1e-4, 3.5e-4, 4e-4) # moments of inertia chosen arbitarily (though they must be distinct)
dt           = 0.001
t            = 0.0
_euler_angles = [0.0, 0.0, 0.0]
plot_counter = 0

'''
Animation
'''

draw_principal_axes()

while True:
    rate(1/dt)
    
    if not running:
        continue
        
#    # update ω
    _w += derivs(_w, _I) * dt
    
#    # update euler angles
    _euler_angles = update_euler_angles(_euler_angles, _w)
    for i in range(3):
        if _euler_angles[i] > 2 * pi or _euler_angles[i] < -2 * pi:
            _euler_angles[i] = _euler_angles[i] % (2 * pi)
    
    # update wingnut orientation
    R = transform(_euler_angles)
    wingnut.axis = vector(R[0][0], R[1][0], R[2][0])
#    wingnut.axis = vector(
#        dot(vector(R[0][0], R[0][1], R[0][2]), wingnut.axis),
#        dot(vector(R[1][0], R[1][1], R[1][2]), wingnut.axis),
#        dot(vector(R[2][0], R[2][1], R[2][2]), wingnut.axis)
#    )
    
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
