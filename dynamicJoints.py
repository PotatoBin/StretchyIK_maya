def makeDynamicJoints():
    selected_joints = cmds.ls(selection=True, type='joint')
    if len(selected_joints) != 2:
        cmds.error("두 개의 조인트를 선택해야 합니다.")

    start_joint = selected_joints[0]
    end_joint = selected_joints[1]

    joint_chain = cmds.listRelatives(start_joint, ad=True, type='joint')
    joint_chain.reverse()

    joint_chain.insert(0, start_joint)
    
    positions = [cmds.xform(joint, q=True, ws=True, t=True) for joint in joint_chain]

    curve = cmds.curve(p=positions, d=3)

    cmds.select(curve)
    
    mel.eval('makeCurvesDynamic 2 { "0", "0", "1", "1", "0"}')
       
    follicle = cmds.ls(type='follicle')[-1]
    hair_system = cmds.ls(type='hairSystem')[-1]
    output_curve = cmds.listConnections(follicle + ".outCurve")[0] 
    
    ik_handle = cmds.ikHandle(sj=start_joint, ee=end_joint, c=output_curve, sol='ikSplineSolver', ccv=False, pcv=False)[0]

    cmds.setAttr(follicle + ".pointLock", 1)
    cmds.setAttr(follicle + ".overrideDynamics", 1)
    cmds.setAttr(hair_system + ".startCurveAttract", 1)

makeDynamicJoints()
