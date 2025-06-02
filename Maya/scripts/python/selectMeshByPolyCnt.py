#
# for more infomation: dungcq@fe.edu.vn
#
import maya.cmds as cmds

def selectMeshByPolyCnt(count):
    """
    Selects all mesh objects in the scene that have a specific number of polygons (faces).

    Args:
        count (int): The number of polygons to search for.
    """
    # List all objects in the scene of type "mesh".
    meshes = cmds.ls(type="mesh")
    # Initialize an empty list to store the names of meshes that match the polygon count.
    matching_meshes = []
    # Iterate through each mesh found in the scene.
    for m in meshes:
        # Get the polygon (face) count of the current mesh.
        poly_count = cmds.polyEvaluate(m, face=True)
        # Check if the polygon count of the current mesh matches the target 'count'.
        if poly_count == count:
            # If the counts match, add the name of the mesh to the 'matching_meshes' list.
            matching_meshes.append(m)

    # Select all the meshes that were added to the 'matching_meshes' list.
    if matching_meshes:
        cmds.select(matching_meshes)
        print(f"Selected meshes with {count} polygons: {matching_meshes}")
    else:
        cmds.select(clear=True)
        print(f"No meshes found with {count} polygons.")

# Example usage: Select all meshes with exactly 18 polygons.
selectMeshByPolyCnt(18)
