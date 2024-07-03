import omni
import random
# import omni.isaac.lab.sim as sim_utils
# import omni.isaac.lab.utils.math as math_utils
# from omni.isaac.lab.assets import RigidObject, RigidObjectCfg
# from omni.isaac.lab.sim import SimulationContext
from pxr import UsdGeom, Gf, Sdf, Usd, PhysxSchema, UsdShade, UsdPhysics
import omni.physx

# Function to drop a cube into the scene
def drop_cube():


    #random location 

    position_range = 4.5
    
    # Generate random coordinates
    x = random.uniform(-position_range, position_range)
    y = random.uniform(-position_range, position_range)
    z = 3.5 #random.uniform(0, position_range)

    stage = omni.usd.get_context().get_stage()
    cube_path = Sdf.Path("/World/Cube")

    # Create the cube if it doesn't exist
    if not stage.GetPrimAtPath(cube_path):
        UsdGeom.Cube.Define(stage, cube_path)

    # Set cube attributes
    cube_prim = stage.GetPrimAtPath(cube_path)
    cube_prim.GetAttribute("size").Set(.5)

    # Set the cube's position
    xform = UsdGeom.Xformable(cube_prim)
    xform.AddTranslateOp().Set(Gf.Vec3f(-.5, -.1, 0))

    # Add physics properties
    physxRigidBodyAPI = PhysxSchema.PhysxRigidBodyAPI.Apply(cube_prim)
    UsdPhysics.MassAPI.Apply(cube_prim).CreateMassAttr().Set(1.0)  # Set mass of the cube

    # Enable gravity
    physxRigidBodyAPI.CreateDisableGravityAttr().Set(False)

    # Add collision
    collisionAPI = UsdPhysics.CollisionAPI.Apply(cube_prim)

    # Add material and set color to red
    material = UsdShade.Material.Define(stage, f"{cube_path}/RedMaterial")
    shader = UsdShade.Shader.Define(stage, f"{cube_path}/RedMaterial/Shader")
    shader.CreateIdAttr("UsdPreviewSurface")
    shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set(Gf.Vec3f(1, 1, 0))  # Red color
    material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")

    # Bind the material to the cube
    UsdShade.MaterialBindingAPI(cube_prim).Bind(material)

    # # Ensure physics simulation is enabled
    # if not stage.GetPrimAtPath("/World/PhysicsScene"):
    #     UsdPhysics.Scene.Define(stage, "/World/PhysicsScene")

# def make_rigid():

#     # Initialize the simulation context
#     context = omni.usd.get_context()
#     stage = context.get_stage()

#     # Function to add collision and physics
#     def add_collision_and_physics(prim_path):
#         # Get the Prim object
#         prim = stage.GetPrimAtPath(prim_path)
        
#         if not prim.IsValid():
#             print(f"Invalid prim: {prim_path}")
#             return

#         # Ensure the prim is a geometric type that can have physics applied
#         if not prim.IsA(UsdGeom.Xform):
#             print(f"Skipping non-geom prim: {prim_path}")
#             return

#         # Add collision
#         #collision_api = omni.physx.PhysxCollisionAPI.Apply(prim)
#         collision_api = UsdPhysics.CollisionAPI.Apply(prim)
#         if not collision_api:  
#             print(f"Failed to apply collision to: {prim_path}")
#             return
        
#         # Add rigid body physics
#         #rigid_body_api = omni.physx.PhysxRigidBodyAPI.Apply(prim)
#         rigid_body_api = PhysxSchema.PhysxRigidBodyAPI.Apply(prim)
#         if not rigid_body_api:
#             print(f"Failed to apply rigid body physics to: {prim_path}")
#             return
        
#         #rigid_body_api.CreateMassAttr().Set(1.0)  # Set mass
#         UsdPhysics.MassAPI.Apply(prim).CreateMassAttr().Set(1.0)
#         #rigid_body_api.CreateRigidBodyEnabledAttr().Set(True)  # Enable rigid body

#     # Traverse all objects in the scene
#     def traverse_prims(prim):
#         if not prim.IsValid():
#             print(f"Invalid prim during traversal: {prim.GetPath().pathString}")
#             return

#         for child in prim.GetChildren():
#             add_collision_and_physics(child.GetPath().pathString)
#             traverse_prims(child)

#     # Start traversal from the root
#     #root_prim = stage.GetDefaultPrim()
#     root_prim = stage.GetPrimAtPath("/World/office")
#     if root_prim.IsValid():
#         traverse_prims(root_prim)
#     else:
#         print("Invalid root prim")

