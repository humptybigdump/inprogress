import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Workshop_A7") #Hier muss der Name der Datei angepasst werden!!!
oDesign = oProject.SetActiveDesign("Maxwell2DDesign1") #Und hier der ensprechende Design das vorhanden ist.
oDesign.ChangeProperty(
	[
		"NAME:AllTabs",
		[
			"NAME:LocalVariableTab",
			[
				"NAME:PropServers", 
				"LocalVariables"
			],
			[
				"NAME:NewProps",
				[
					"NAME:Amp",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "1A"
				],
				[
					"NAME:rpm",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "1rpm"
				],
				[
					"NAME:sec",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "1s"
				],
				[
					"NAME:p",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "4"
				],
				[
					"NAME:speed_rpm",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "7000"
				],
                [
					"NAME:omega_rad",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "speed_rpm/60*2*pi*p"
				],
				[
					"NAME:Thet_deg",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "44.85"
				],
				[
					"NAME:Thet",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "(Thet_deg+90)*pi/180"
				],
				[
					"NAME:ini_pos",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "-37.5"
				],
				[
					"NAME:Strom_eff",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "120"
				],
                [
					"NAME:I_eff",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "Strom_eff*Amp"
				],
				[
					"NAME:I_U",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "I_eff*sqrt(2)*cos((omega_rad*Time+Thet))"
				],
				[
					"NAME:I_V",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "I_eff*sqrt(2)*cos((omega_rad*Time-2*pi/3)+Thet)"
				],
				[
					"NAME:I_W",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "I_eff*sqrt(2)*cos((omega_rad*Time-4*pi/3)+Thet)"
				],
				[
					"NAME:T_Periode",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "sec/(speed_rpm/60*p)"
				],
				[
					"NAME:Zeit_Schritte",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "50"
                ],
                [
					"NAME:V_Angle",
					"PropType:="		, "VariableProp",
					"UserDef:="		, True,
					"Value:="		, "7.5deg"
                ]
			]
		]
	])
