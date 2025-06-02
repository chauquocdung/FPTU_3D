#
# for more infomation: dungcq@fe.edu.vn
#
import maya.cmds

def restoreTrans(objName):
    """
    Resets the transformation (txyz) of an object while preserving its world space position.

    Args:
        objName (str): The name of the object to restore the transform for.
    """
    # Query the current world space pivot point of the object.
    # The pivot point is used as a reference for the object's world position.
    pivOrg = cmds.xform(objName, query=True, worldSpace=True, piv=True)

    # Move the object to the world origin (0, 0, 0) using the inverse of its pivot point.
    # This effectively brings the object's pivot to the center of the world.
    cmds.xform(objName, worldSpace=True, t=[pivOrg[0] * -1, pivOrg[1] * -1, pivOrg[2] * -1])

    # Apply the object's current transformation as its new identity (no translation, rotation, scale).
    # This "freezes" the current world space transformation into the object's local transform.
    cmds.makeIdentity(objName, apply=True, t=True, r=True, s=True)

    # Move the object back to its original world space position using the previously queried pivot point.
    # Since the local transform is now the identity, this effectively places the object back
    # where it was before the makeIdentity operation.
    cmds.xform(objName, worldSpace=True, t=[pivOrg[0], pivOrg[1], pivOrg[2]])

if __name__ == "__main__":
    # Get a list of all currently selected objects (using long names for clarity).
    sl = cmds.ls(sl=True, l=True)
    # Iterate through each selected object.
    for s in sl:
        # Call the restoreTrans function to reset the transformation of the current object.
        restoreTrans(s)
