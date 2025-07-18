import maya.cmds as cmds
import maya.mel as mel

# Create warp threads
def create_warp_threads(num_threads=10, spacing=1.0):
    warp_group = cmds.group(em=True, name='warpThreads_grp')
    warp_threads = []
    for i in range(num_threads):
        thread = cmds.polyPlane(w=0.1, h=5, sx=1, sy=10, name=f'warpThread_{i}')[0]
        cmds.move(i * spacing, 0, 0, thread)
        cmds.parent(thread, warp_group)
        warp_threads.append(thread)
    return warp_threads

# Create heddles
def create_heddles(num_heddles=2, spacing=2.0):
    heddle_group = cmds.group(em=True, name='heddles_grp')
    heddles = []
    for i in range(num_heddles):
        heddle = cmds.polyCube(w=spacing * 5, h=0.2, d=0.2, name=f'heddle_{i}')[0]
        cmds.move(spacing * i, 1.5, 0, heddle)
        cmds.parent(heddle, heddle_group)
        heddles.append(heddle)
    return heddles

# Animate heddles
def animate_heddles(heddles, lift_height=1.0, frame_interval=20):
    for i, heddle in enumerate(heddles):
        start_frame = i * frame_interval
        cmds.setKeyframe(heddle, attribute='translateY', t=start_frame, v=1.5)
        cmds.setKeyframe(heddle, attribute='translateY', t=start_frame + frame_interval // 2, v=1.5 + lift_height)
        cmds.setKeyframe(heddle, attribute='translateY', t=start_frame + frame_interval, v=1.5)

# Create shuttle
def create_shuttle():
    shuttle = cmds.polyCube(w=0.5, h=0.2, d=0.2, name='shuttle')[0]
    cmds.move(0, 0.5, -1, shuttle)
    cmds.setKeyframe(shuttle, attribute='translateX', t=0, v=0)
    cmds.setKeyframe(shuttle, attribute='translateX', t=40, v=9)
    cmds.setKeyframe(shuttle, attribute='translateX', t=80, v=0)
    return shuttle

# Setup nCloth and passive colliders
def setup_ncloth(warp_threads, colliders, attract_value=0.2):
    for thread in warp_threads:
        cmds.select(thread)
        cmds.nClothCreate()
        shape = cmds.ls(sl=1)[0]
        # Get the shape node of the thread
        #shape_node = cmds.listRelatives(thread, shapes=True)[0]
        # Set inputMeshAttract
        cmds.setAttr(f"{shape}.inputMeshAttract", attract_value)
        cmds.setAttr(f"{shape}.stretchResistance", 100)
        cmds.setAttr(f"{shape}.compressionResistance", 100)
        cmds.setAttr(f"{shape}.bendResistance", 0.5)
        cmds.setAttr(f"{shape}.damp", 0.1)

    for collider in colliders:
        #cmds.select(collider)
        #cmds.makeCollideNCloth()
        
        mel.eval('select "heddle_0"; makeCollideNCloth;')


def tune_warp_threads(warp_prefix="warpThread_", count=10):
    for i in range(count):
        thread = f"{warp_prefix}{i}"
        shape = cmds.listRelatives(thread, shapes=True)[0]
        
        # Set nCloth attributes
        cmds.setAttr(f"{shape}.inputMeshAttract", 0.3)
        cmds.setAttr(f"{shape}.stretchResistance", 100)
        cmds.setAttr(f"{shape}.compressionResistance", 100)
        cmds.setAttr(f"{shape}.bendResistance", 0.5)
        cmds.setAttr(f"{shape}.damp", 0.1)



# Run the setup
warp_threads = create_warp_threads(num_threads=10, spacing=1.0)
heddles = create_heddles(num_heddles=2, spacing=2.0)
animate_heddles(heddles, lift_height=1.0, frame_interval=20)
shuttle = create_shuttle()
setup_ncloth(warp_threads, heddles + [shuttle])
#tune_warp_threads()
print("✅ Weaving loom simulation setup completed.")
