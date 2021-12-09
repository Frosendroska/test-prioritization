from pathlib import Path


def parse_projects_file(prefix=Path("")):
    projects = []
    with open(prefix / Path("projects.txt"), "r") as file:
        for line in file:
            projects += line.rstrip().split("#")[0].split()
    return projects


count = [
    (1456, "Exposed_TestOracle"),  # 139 tests
    (1293, "Kotlin_dev_CompilerAndPlugin_191"),  # 23k tests
    (1262, "Kotlin_dev_CompilerAndPlugin_192"),  # 23k tests
    (2312, "Kotlin_dev_CompilerAndPlugin_as34"),  # 22k tests
    (2319, "Kotlin_dev_CompilerAndPlugin_as35"),  # 23k tests
    (1279, "Kotlin_dev_GradleIntegrationTests"),  # 420 tests
    (2336, "Kotlin_dev_CompilerAndPlugin_183"),  # 25k tests
    (1140, "Kotlin_dev_Aggregate"),  # 100k tests, not fully downloaded
]

count2 = [
    (106, "Kotlin_master_Aggregate"),
    (107, "IdeaVim_Nvim"),
    (107, "KotlinTools_Ktor_BuildGradleWindows"),
    (107, "MPS_20191_Distribution_BuildNumber"),
    (111, "MPS_20192_Distribution_Statistics"),
    (113, "bt554"),
    (114, "bt603"),
    (114, "Kotlin_KotlinX_Html"),
    (115, "bt744"),
    (117, "bt367"),
    (118, "TeamCityPluginsByJetBrains_Unsorted_RingUISandbox"),
    (120, "Kotlin_Performance_IdeaPluginPerformanceTests_Vplus1"),
    (123, "Kotlin_TypeScriptDeclarationToKotlinConverter_DukatTranspileConverter"),
    (123, "Kotlin_PluginsCompatibilityCheck_As35Trunk13"),
    (124, "Kotlin_PluginsCompatibilityCheck_As33Trunk13"),
    (128, "Kotlin_master_CompilerAndPlugin_173"),
    (131, "MPS_20212_Distribution_BuildNumber"),
    (131, "Kotlin_PluginsCompatibilityCheck_As34Trunk13"),
    (131, "Kotlin_master_CompilerAndPlugin_as23"),
    (132, "Kotlin_master_CompilerAndPlugin_172"),
    (133, "Kotlin_master_CompilerAndPlugin_163"),
    (134, "Kotlin_master_CompilerTests"),
    (134, "Kotlin_master_CompilerAndPlugin_171"),
    (134, "Kotlin_master_CompilerAndPlugin_as30"),
    (136, "VMprofPython_TestsPython27onMac"),
    (136, "bt1058"),
    (136, "Kotlin_master_CompilerAndPlugin_NoTests"),
    (138, "bt992"),
    (138, "MPS_34_BuildNumber"),
    (139, "bt1008"),
    (142, "KotlinTools_Ktor_BuildLinuxCoroutinesSnapshot"),
    (145, "Kotlin_master_CompilerBootstrapNoTests"),
    (147, "KotlinTools_Ktor_BuildGradleMac"),
    (155, "IdeaVim_Qodana"),
    (163, "VMprofPython_TestsPython27onLinux"),
    (164, "VMprofPython_TestsPython34onLinux"),
    (164, "bt1059"),
    (165, "VMprofPython_TestsPython35onLinux"),
    (165, "bt1060"),
    (169, "ProjectsWrittenInKotlin_SysKotlin"),
    (187, "Kotlin_KotlinPublic_BootstrapTestFir_LINUX"),
    (188, "bt366"),
    (193, "IntellijIdeaPlugins_Rust_192_TestIdea"),
    (194, "IntellijIdeaPlugins_Rust_192_TestCLion"),
    (195, "OpenSourceProjects_Betaflight_BetaflightConfigurator_Windows"),
    (200, "KotlinTools_KotlinxCoroutines_NightlyStressWindows"),
    (201, "KotlinTools_KotlinxCoroutines_NightlyStress"),
    (201, "Kotlin_Performance_IdeaPluginPerformanceTests"),
    (212, "MPS_20192_Distribution_IdeaPlugIn"),
    (227, "MPS_20192_Distribution_TestBinaries"),
    (227, "MPS_20192_Distribution_TestsFromIdeaProject"),
    (227, "MPS_20192_Distribution_IdeaPlugInLatestIdeaBuild"),
    (227, "MPS_20192_Distribution_WindowsInstaller"),
    (227, "MPS_20192_Distribution_MacInstaller"),
    (227, "MPS_20192_Distribution_TestTypesystem"),
    (227, "MPS_20192_Distribution_LinuxDistribution"),
    (229, "Kotlin_KotlinPublic_Artifacts"),
    (229, "MPS_20192_Distribution_Binaries"),
    (229, "MPS_20192_Distribution_Extensions"),
    (244, "OpenSourceProjects_Hsqldb_HsqldbTrunkIdea"),
    (252, "bt413"),
    (256, "Kotlin_KotlinPublic_Aggregate"),
    (270, "NUnit_NUnit3_FrameworkMSBuild_FrameworkWindowsNet45"),
    (278, "NUnit_NUnit3_FrameworkMSBuild_FrameworkWindowsMono40"),
    (290, "IdeaVim_IdeaVimEasyMotion_BuildMaster"),
    (337, "NUnit_NUnit3_FrameworkMSBuild_FrameworkWindowsNet20"),
    (342, "cb_bt350"),
    (359, "bt131"),
    (362, "bt130"),
    (409, "NUnit_NUnit3_FrameworkMSBuild_FrameworkWindowsNet40"),
    (418, "IntellijIdeaPlugins_Rust_TestEapCLion"),
    (427, "bt1155"),
    (427, "IntellijIdeaPlugins_Rust_EapIdea_TestsRust"),
    (436, "NUnit_NUnit3_BuildAndTest_WindowsNet45"),
    (436, "bt778"),
    (437, "NUnit_NUnit3_BuildAndTest_WindowsNet20"),
    (437, "bt779"),
    (438, "NUnit_NUnit3_BuildAndTest"),
    (438, "bt776"),
    (443, "Kotlin_KotlinPublic_CompilerDist"),
    (449, "MPS_20192_Distribution_BuildNumber"),
    (466, "Kotlin_KotlinX_Css"),
    (473, "bt565"),
    (473, "NUnit_NUnit3_FrameworkMSBuild_FrameworkLinuxMono40"),
    (527, "bt780"),
    (698, "bt133"),
    (703, "bt132"),
    (739, "bt136"),
    (1031, "bt425"),
    (1069, "bt157"),
    (1291, "bt419"),
    (1292, "bt420"),
    (1295, "bt704"),
    (1295, "bt422"),
    (1299, "bt421"),
]
