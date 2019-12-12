.. Copyright (c) 2019 Audi Electronics Venture GmbH. All Rights Reserved.

.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

Application in Conan recipes
++++++++++++++++++++++++++++

.. contents::


Referencing the generator in a recipe
*************************************

To be able to use the ADTF2Generator in a recipe, it first has to be defined as a dependency. This is usually done in the recipe for an ADTF configuration. Then the generator is specified. The virtual generator is optional here, as – if it exists – it is used internally by the ADTF2Generator to generate the "activate" and "deactivate" scripts.

.. code-block:: python

    requires = "ADTF2Generator/[1]@CoRTEX/stable"
    generators = "ADTF2Generator", "virtualenv"


Definition of an ADTF project
*****************************

An ADTF project has to be defined using the package_info() method. This is done as a list of dictionaries, as the recipe or package could also include multiple configurations.

.. code-block:: python

    def package_info(self):
        # define the list of dictionaries which describe the ADTF project and what to generate
        self.user_info.ADTF_PROJECTS=[{"PROJECT_PATH": os.path.join(self.package_folder, "my_project_directory", "my_project_name.prj"),
                                        "CONFIG_PATH": os.path.join(self.package_folder, "my_project_directory", "config", "system.xml"),
                                        "MANIFESTS_USE": ["adtf_devenv.manifest", "adtf_runtime.manifest"],
                                        "START_PARAMETER": "-run",
                                        "GLOBALS_USE": ["globals.xml"]}]

The following parameters are defined in the example above:

* **PROJECT_PATH**: Indicates the full path to the ADTF project
* **CONFIG_PATH**: (Optional) Indicates the full path to the system.xml. This is usually only required for the adtf_console, however, as this configuration includes no ADTF project tree that could load projects.
* **MANIFESTS_USE**: (Optional) This can be used to control which start scripts are to be generated for the project. If this is not set, all ADTF start manifests from the ADTF bin directory are used as a basis and a start script is generated for each.
* **START_PARAMETER**: (Optional) This can be used to transfer additional parameters for each project to ADTF (e.g. -run, -stdout -quit, -active, etc.; refer to the ADTF documentation for this). 
* **GLOBALS_USE**: (Optional) ADTF itself delivery two globals.xml files, one for the GUI and one for the console application. If this value is restricted to "globals.xml", no adtf_console start script is generated, even if it is defined under MANIFESTS_USE. Additionally (with version 1.1.1 of the Generator) one can define an absolute path to a custom globals.xml which should be stored alongside with the project.

The following is an example for several ADTF configurations within a package.

.. code-block:: python

    def package_info(self):
        # define the list of dictionaries which describe the ADTF project and what to generate
        self.user_info.ADTF_PROJECTS=[{"PROJECT_PATH": os.path.join(self.package_folder, "my_project_directory", "my_project_name.prj"),
                                        "CONFIG_PATH": os.path.join(self.package_folder, "my_project_directory", "config", "system.xml"),
                                        "MANIFESTS_USE": ["adtf_devenv.manifest", "adtf_runtime.manifest"],
                                        "START_PARAMETER": "-run",
                                        "GLOBALS_USE": ["globals.xml"]},
                                    {"PROJECT_PATH": os.path.join(self.package_folder, "my_project_directory2", "my_project_name2.prj"),
                                        "CONFIG_PATH": os.path.join(self.package_folder, "my_project_directory2", "config", "system.xml"),
                                        "MANIFESTS_USE": ["adtf_runtime.manifest"],
                                        "START_PARAMETER": ""}]



Definition of ADTF filters/plugins
**********************************

Only the description of the plugin path is required for an ADTF filter. This is generated into the respective `globals.xml`. This once again includes a list, so multiple plugins can be referenced.

.. note:: The ADTF notation (with `*.plb` or `**.plb`) can be used as these values are entered directly without resolving them again first. 

.. code-block:: python

    def package_info(self):
        self.env_info.MY_PACKAGE_DIR=self.package_folder
        self.user_info.ADTF_PLUGINS=[os.path.join(self.package_folder, "bin", "*.plb")]


Definition of ADTF services
***************************

An ADTF service always describes itself and its plugin in a manifest. Therefore, only the path to the `.manifest` has to be defined for an ADTF service. Once again, the paths are not evaluated further, and can therefore be made directly in ADTF notation.

.. code-block:: python

    def package_info(self):
        self.user_info.ADTF_MANIFESTS=[os.path.join(self.package_folder, "bin", "*.manifest")]

Definition of ADTF custom manifests (own ADTF launcher manifests)
*****************************************************************

Two different types have to be distinguished for ADTF manifests.

#. ADTF service manifest: describes an individual service or multiple services, and is included by the launcher manifest. It is not possible to start a complete ADTF session with a conventional ADTF service manifest.
#. ADTF launcher manifest: describes an ADTF basic system consisting of the ADTF core services that are mandatory, and includes additional ADTF service manifests for ADTF services originating from other packages.

The latter (i.e. the starting point for ADTF) can also originate from other packages than ADTF itself (also refer to the examples "custom_runtime_manifest"). 

.. important:: Only the services from the ADTF package itself can be referenced. The ADTF_MANIFESTS have to be used for all additional services and their paths.

.. code-block:: python

    def package_info(self):
        # define the path to the customized ADTF manifest
        self.user_info.ADTF_CUSTOM_MANIFESTS=[os.path.join(self.package_folder, "custom_runtime.manifest")]

The manifest package then only has to be included in the dependency tree to be considered by the generator (e.g. as a dependency of an ADTF configuration).


Definition of ADTF description (DDL) files
******************************************

ADTF uses description files (DDL - Data Definition Language) for describing data structures. These can be defined as follows, to then be included into the launcher manifests.

.. code-block:: python

    def package_info(self):
        # define the path to the description file
        self.user_info.ADTF_DESCRIPTIONS=[os.path.join(self.package_folder, "simple_adtf.description")]


The description package then only has to be included in the dependency tree to be considered by the generator (e.g. as a dependency of an ADTF configuration).


Definition of manifest dependencies to be removed
*************************************************

In some use cases, it can be practical to remove manifests (e.g. from ADTF tool boxes) from the overall configuration, and then replace them with custom manifests.

To do so, only the following must be entered to remove manifests:

.. code-block:: python

    def package_info(self):
        # just define the name of the dependency which manifests should not be added or should be removed
        self.user_info.ADTF_REMOVE_MANIFESTS_DEPS=["ADTFDeviceToolbox"]

For this, only the name(s) of the manifest dependencies to be removed must be stated in the form of a list.

Definition of plugin dependencies to be removed
***********************************************

In some use cases, it can be practical to remove plugins (e.g. from ADTF tool boxes) from the overall ADTF configuration, and then replace them with a custom plugins list.

Only the following must be entered to remove plugins:

.. code-block:: python

    def package_info(self):
        # just define the name of the dependency which plugins should not be added or should be removed
        self.user_info.ADTF_REMOVE_PLUGINS_DEPS=["ADTFDeviceToolbox"]

For this, only the name(s) of the plugin dependencies to be removed has to be stated, in the form of a list.

Definition of description dependencies to be removed
****************************************************

In some use cases, it can be practical to remove descriptions (e.g. from ADTF tool boxes) from the overall ADTF configuration, and then replace them with own descriptions.

Only the following must be entered to remove descriptions:

.. code-block:: python

    def package_info(self):
        # just define the name of the dependency which descriptions should not be added or should be removed
        self.user_info.ADTF_REMOVE_DESCRIPTIONS_DEPS=["ADTFDeviceToolbox"]

For this, only the name(s) of the description dependencies to be removed must be stated, in the form of a list.

Definition of project dependencies to be removed
************************************************

In some use cases, it can be practical to remove projects (e.g. from ADTF tool boxes) from the overall ADTF configuration, and then replace them with own projects.

Only the following must be entered to remove projects:

.. code-block:: python

    def package_info(self):
        # just define the name of the dependency which projects should not be added or should be removed
        self.user_info.ADTF_REMOVE_PROJECTS_DEPS=["ADTFDeviceToolbox"]

For this, only the name(s) of the project dependencies to be removed must be stated, in the form of a list.

Definition of custom manifest dependencies to be removed (own ADTF launcher manifests)
**************************************************************************************

In some use cases, it can be practical to remove custom manifests from the overall ADTF configuration and then replace them with own custom manifests.

Only the following must be entered to remove custom manifests:

.. code-block:: python

    def package_info(self):
        # just define the name of the dependency which projects should not be added or should be removed
        self.user_info.ADTF_REMOVE_CUSTOM_MANIFESTS_DEPS=["MyCustomManifestPackage"]

For this, only the name(s) of the custom manifest dependencies to be removed must be stated, in the form of a list.

Use of ADTF subconfigurations
+++++++++++++++++++++++++++++

There are two options for integrating/using ADTF2 subconfigurations. The choice depends on the "main system.xml" and how it integrates the subconfiguration.


Option 1: integration through relative paths
********************************************

If the subconfiguration is integrated in the "main system.xml" with a relative path, the subconfiguration has to be copied/imported into the main configuration. This can be achieved with the Conan `imports()` method.

.. code-block:: python

    from conans import ConanFile

    class ADTF2MainConfigConan(ConanFile):
        name = "ADTF2MainConfig"
        version = "1.0.0"
        build_requires = "ADTF2SubConfig/1.0.0@user/testing"
        keep_imports = True

        def imports(self):
            self.copy(pattern="*", dst="path/to/subconfig", src="probably/not/required/to/define", root_package="ADTF2SubConfig")

        def package(self):
            self.copy("*")
    ...


.. important:: If the subconfiguration includes dependencies to ADTF2 filters, services, descriptions or other packages, these have to be transferred to the main configuration, because the use of `build_requires` "interrupts" the dependency tree.


Option 2: integration through environment variables
***************************************************

The much neater variant is to integrate the subconfiguration in the main configuration using environment variables. This means that the subconfiguration only has to be defined as a requirement, and the `package_info` of the subconfiguration has to define the environment variable.

.. code-block:: python

    from conans import ConanFile

    class ADTF2MainConfigConan(ConanFile):
        name = "ADTF2MainConfig"
        version = "1.0.0"
        requires = "ADTF2SubConfig/1.0.0@user/testing"
        
        def package(self):
            self.copy("*")
    ...


.. code-block:: python

    from conans import ConanFile

    class ADTF2SubConfigConan(ConanFile):
        name = "ADTF2SubConfig"
        version = "1.0.0"

        def package(self):
            self.copy("*")

        def package_info(self):
            self.env_info.vars["%s_DIR" % self.name.upper()] = self.package_folder.replace("\\", "/")
    ...




