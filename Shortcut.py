import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Workshop_A6")
oDesign = oProject.SetActiveDesign("IPM_0")
oModule = oDesign.GetModule("BoundarySetup")
for i in range(1,21):
	oModule.AssignWindingGroup(
		[
			"NAME:Winding_A" + str(i),
			"Type:="		, "Current",
			"IsSolid:="		, True,
			"Current:="		, "I_U/4/5",
			"Resistance:="		, "0ohm",
			"Inductance:="		, "0nH",
			"Voltage:="		, "0mV",
			"ParallelBranchesNum:="	, "1"
		])
        
for j in range(1,21):
    oModule.AddWindingCoils("Winding_A" + str(j), ["A" + str(j), "A"  + str(j) + "_1", "A"  + str(j) + "_2", "A"  + str(j) + "_3", "A"  + str(j) + "_4"])
