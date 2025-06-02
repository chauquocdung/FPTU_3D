#
# for further details: dungcq@fe.edu.vn
#
import maya.cmds as cmds

def convertSelection(selection, fType='transform', tType='mesh'):
    """
    Converts a list of selected objects from one type to another.
    For example, it can take a list of transform nodes and return their corresponding shape nodes (meshes).

    Args:
        selection (list): A list of selected object names.
        fType (str): The type of the input objects (default: 'transform').
        tType (str): The desired output type (default: 'mesh').

    Returns:
        list: A list of lists, where each inner list contains the original transform node and its found shape node [transform_node, shape_node].
              Returns an empty list if no objects of the specified 'fType' are found with the target 'tType' as a child.
    """
    ret = []
    for s in selection:
        # Check if the current selected object is of the specified 'fType' (e.g., 'transform').
        if not cmds.objectType(s) == fType:
            continue
        # List the children of the current object that are of the target 'tType' (e.g., 'mesh').
        # 'c=1' means list children, 'type=tType' filters by type, 'f=1' makes the names full.
        sh = cmds.listRelatives(s, c=1, type=tType, f=1)
        if sh:
            # If a child of the target type is found, add a list containing the transform and the shape to the result.
            ret.append([s, sh[0]])
    return ret

def instance_selected_meshes():
    """
    Instances all selected mesh objects based on the first selected mesh.

    The first selected object's mesh will be used as the base for the instances.
    The subsequent selected objects will have instances of the base mesh created at their
    world space positions, rotations, and scales.
    The original transform nodes of the instanced meshes (except the first) will be deleted.
    """
    # Get a list of selected objects and convert them to pairs of [transform_node, shape_node] for meshes.
    selected_meshes = convertSelection(cmds.ls(selection=True, l=1))

    # Check if we have at least two selected meshes (one base and at least one to instance).
    if not selected_meshes or len(selected_meshes) < 2:
        cmds.warning("Please select at least two mesh objects. The first selected will be the base instance.")
        return

    # The first selected mesh will be our base for instancing. We take both its transform and shape.
    base_mesh_transform, base_mesh_shape = selected_meshes[0]
    # The remaining selected meshes are the ones we want to instance the base mesh onto.
    meshes_to_instance = selected_meshes[1:]

    instance_transforms = []
    original_transforms = []

    # Iterate through the meshes we want to instance onto.
    for transform_node, shape in meshes_to_instance:
        # Store the original transform node so we can delete it later.
        original_transforms.append(transform_node)
        # Query the world transformation matrix of the current object. This matrix contains its position, rotation, and scale.
        matrix = cmds.xform(transform_node, query=True, worldSpace=True, matrix=True)
        # Store this matrix to apply to the new instance.
        instance_transforms.append(matrix)
    print("original_transforms", original_transforms)

    # If we have transformation matrices (meaning there were other selected meshes).
    if instance_transforms:
        # Iterate through the collected transformation matrices.
        for i, matrix in enumerate(instance_transforms):
            # Create a new instance of the base mesh shape. 'leaf=True' ensures we only instance the shape.
            newInstance = cmds.instance(base_mesh_shape, leaf=True)[0]
            # Apply the world transformation matrix of the original object to this new instance.
            cmds.xform(newInstance, worldSpace=True, matrix=matrix)

        # Delete the original transform nodes of the meshes that were instanced.
        cmds.delete(original_transforms)

        print(f"Instanced {len(meshes_to_instance)} objects based on '{base_mesh_transform}'. Original instances deleted.")

    else:
        print("No other meshes selected to instance.")

# This block ensures the function runs only when the script is executed directly (not when imported as a module).
if __name__ == '__main__':
    instance_selected_meshes()
