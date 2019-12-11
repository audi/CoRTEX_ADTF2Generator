# Copyright (c) 2019 Audi Electronics Venture GmbH. All Rights Reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# 

import os

from conans import ConanFile
from conans.model import Generator
from conans.errors import ConanException
from conans.model.version import Version
from conans.util.files import load

def check_convert_to_list(param):
    if isinstance(param, list):
        return param
    elif isinstance(param, str):
        return [param]
    else:
        raise ConanException("The parameter is not of type list or string.")

def eval_var(var):
    try:
        return eval(var)
    except:
        return var

        
class ADTF2Generator(Generator):
    
    _generate_2_dir = None
    @property
    def generate_2_dir(self):
        if not self._generate_2_dir:
            self._generate_2_dir = "ADTF_gen"
        return self._generate_2_dir
        
    @property
    def filename(self):
        pass 
 
                    
    def _get_user_info_list(self, key_word, remove_from_list=[]):
        ui_list = []
        if self.conanfile.user_info and key_word in self.conanfile.user_info.vars:
            entry = eval_var(getattr(self.conanfile.user_info, key_word))
            ui_list.extend(check_convert_to_list(entry))
        for dep, the_vars in self.deps_user_info.items():
            if dep in remove_from_list:
                continue
            if key_word in the_vars.vars:
                entry = eval_var(the_vars.vars[key_word])
                ui_list.extend(check_convert_to_list(entry))
        return ui_list
                
    _ADTF_dep = None
    @property
    def ADTF_dep(self):
        if not self._ADTF_dep:
            for dep_name, dep_cpp_info in self.deps_build_info.dependencies:
#                self.conanfile.output.info("Processing: " + dep_name)
                if dep_name == "ADTF":
                    version = Version(dep_cpp_info.version)
                    if version >= "2.0.0" and version < "3.0.0":
                        self._ADTF_dep = dep_cpp_info
                        break
                
            if not self._ADTF_dep:
                raise ConanException("There is no suitable ADTF 2 dependency defined as requirement.")
        return self._ADTF_dep
    
    _ADTF_bin_dir = None
    @property
    def ADTF_bin_dir(self):
        if not self._ADTF_bin_dir:
            is_debug = True if self.conanfile.settings.get_safe("build_type") == "Debug" else False
            if is_debug:
                self._ADTF_bin_dir = os.path.join(self.ADTF_dep.rootpath, "bin", "debug").replace("\\", "/")
            else:
                self._ADTF_bin_dir = os.path.join(self.ADTF_dep.rootpath, "bin").replace("\\", "/")
        return self._ADTF_bin_dir
    
    _deps_dirs = None
    @property
    def deps_dirs(self):
        if not self._deps_dirs:
            self._deps_dirs = {}
            for dep_name, dep_cpp_info in self.deps_build_info.dependencies:
                self._deps_dirs[dep_name] = dep_cpp_info.rootpath.replace("\\", "/")
        return self._deps_dirs

    
    _ADTF_remove_plugins_deps = None
    @property
    def ADTF_remove_plugins_deps(self):
        if not self._ADTF_remove_plugins_deps:
            self._ADTF_remove_plugins_deps = []
            key_word="ADTF_REMOVE_PLUGINS_DEPS"
            self._ADTF_remove_plugins_deps.extend(self._get_user_info_list(key_word))
        return self._ADTF_remove_plugins_deps
            
    _ADTF_plugins = None
    @property
    def ADTF_plugins(self):
        if not self._ADTF_plugins:
            self._ADTF_plugins = []
            key_word="ADTF_PLUGINS"
            self._ADTF_plugins.extend(self._get_user_info_list(key_word, self.ADTF_remove_plugins_deps))
        return self._ADTF_plugins

    _ADTF_remove_manifests_deps = None
    @property
    def ADTF_remove_manifests_deps(self):
        if not self._ADTF_remove_manifests_deps:
            self._ADTF_remove_manifests_deps = []
            key_word="ADTF_REMOVE_MANIFESTS_DEPS"
            self._ADTF_remove_manifests_deps.extend(self._get_user_info_list(key_word))
        return self._ADTF_remove_manifests_deps
        
    _ADTF_manifests = None
    @property
    def ADTF_manifests(self):
        if not self._ADTF_manifests:
            self._ADTF_manifests = []
            key_word="ADTF_MANIFESTS"
            self._ADTF_manifests.extend(self._get_user_info_list(key_word, self.ADTF_remove_manifests_deps))
        return self._ADTF_manifests
           
    _ADTF_remove_descriptions_deps = None
    @property
    def ADTF_remove_descriptions_deps(self):
        if not self._ADTF_remove_descriptions_deps:
            self._ADTF_remove_descriptions_deps = []
            key_word="ADTF_REMOVE_DESCRIPTIONS_DEPS"
            self._ADTF_remove_descriptions_deps.extend(self._get_user_info_list(key_word))
        return self._ADTF_remove_descriptions_deps
    
    _ADTF_descriptions = None
    @property
    def ADTF_descriptions(self):
        if not self._ADTF_descriptions:
            self._ADTF_descriptions = []
            key_word="ADTF_DESCRIPTIONS"
            self._ADTF_descriptions.extend(self._get_user_info_list(key_word, self.ADTF_remove_descriptions_deps))
        return self._ADTF_descriptions
           
    _ADTF_remove_projects_deps = None
    @property
    def ADTF_remove_projects_deps(self):
        if not self._ADTF_remove_projects_deps:
            self._ADTF_remove_projects_deps = []
            key_word="ADTF_REMOVE_PROJECTS_DEPS"
            self._ADTF_remove_projects_deps.extend(self._get_user_info_list(key_word))
        return self._ADTF_remove_projects_deps
    
    _ADTF_projects = None
    @property
    def ADTF_projects(self):
        if not self._ADTF_projects:
            self._ADTF_projects = []
            key_word="ADTF_PROJECTS"
            self._ADTF_projects.extend(self._get_user_info_list(key_word, self.ADTF_remove_projects_deps))
        return self._ADTF_projects
           
    _ADTF_remove_custom_manifests_deps = None
    @property
    def ADTF_remove_custom_manifests_deps(self):
        if not self._ADTF_remove_custom_manifests_deps:
            self._ADTF_remove_custom_manifests_deps = []
            key_word="ADTF_REMOVE_CUSTOM_MANIFESTS_DEPS"
            self._ADTF_remove_custom_manifests_deps.extend(self._get_user_info_list(key_word))
        return self._ADTF_remove_custom_manifests_deps
    
    _ADTF_custom_manifests = None
    @property
    def ADTF_custom_manifests(self):
        if not self._ADTF_custom_manifests:
            self._ADTF_custom_manifests = []
            key_word="ADTF_CUSTOM_MANIFESTS"
            self._ADTF_custom_manifests.extend(self._get_user_info_list(key_word, self.ADTF_remove_custom_manifests_deps))
        return self._ADTF_custom_manifests
   
    def generate_globals(self, globals_in):
        
        from xml.dom import minidom
        
        content = load(globals_in).replace(u'\n', u'')
        dom = minidom.parseString(content)
        
        gen_settings = dom.getElementsByTagName("general_settings")
        if len(gen_settings) > 0:
            properties = gen_settings[0].getElementsByTagName("property")
            
            for prop in properties:
                name = prop.getAttribute("name")
                if name == "media_description_files":
                    oldVal = prop.getAttribute("value")
                    prop.setAttribute("value", oldVal + (";" if len(self.ADTF_descriptions) > 0 else "") + ";".join(self.ADTF_descriptions))
        
        plugins_group = dom.getElementsByTagName("plugins")
        if len(plugins_group) > 0:
            plugins = plugins_group[0].getElementsByTagName("plugin")
            for plg in plugins:
                plugins_group[0].removeChild(plg)
                plg.unlink()
            adtf_bin_plugins = dom.createElement("plugin")
            adtf_bin_plugins.setAttribute("optional", "true")
            adtf_bin_plugins.setAttribute("url", self.ADTF_bin_dir + "/*.plb")
            plugins_group[0].appendChild(adtf_bin_plugins)
            
            for adtf_plugins in self.ADTF_plugins:
                new_plugin = dom.createElement("plugin")
                new_plugin.setAttribute("optional", "true")
                new_plugin.setAttribute("url", adtf_plugins.replace("\\", "/"))
                plugins_group[0].appendChild(new_plugin)
        
        result = dom.toprettyxml().replace("<?xml version=\"1.0\" ?>", "<?xml version=\"1.0\" encoding=\"iso-8859-1\" standalone=\"no\"?>\n")
        result = "\n".join(str(line) for line in result.splitlines() if line.strip())
        
        return result
    
    def generate_manifest(self, manifest_in):
        
        from xml.dom import minidom
        
        content = load(manifest_in).replace(u'\n', u'')
        dom = minidom.parseString(content)
        
        plugins_group = dom.getElementsByTagName("plugins")
        if len(plugins_group) > 0:
            plugins = plugins_group[0].getElementsByTagName("plugin")
            
            for plugin in plugins:
                oldVal = plugin.getAttribute("url")
                plugin.setAttribute("url", self.ADTF_bin_dir + "/" + oldVal)
        
        manifests_group = dom.getElementsByTagName("manifests")
        if len(manifests_group) > 0:
            manifests = manifests_group[0].getElementsByTagName("manifest")
            for manifest in manifests:
                manifests_group[0].removeChild(manifest)
                manifest.unlink()
                    
            for adtf_manifests in self.ADTF_manifests:
                new_manifest = dom.createElement("manifest")
                new_manifest.setAttribute("optional", "false")
                new_manifest.setAttribute("url", adtf_manifests.replace("\\", "/"))
                manifests_group[0].appendChild(new_manifest)
        
        environment_group = dom.getElementsByTagName("environment")
        if len(environment_group) == 0:
            environment = dom.createElement("environment")
            root = dom.getElementsByTagName("adtf:manifest")
            root[0].appendChild(environment)
        else:
            environment = environment_group[0]
        
        for dep_name, dep_dir in self.deps_dirs.items():
            var = dom.createElement("variable")
            var.setAttribute("name", dep_name + "_MODULE_PATH")
            var.setAttribute("value", dep_dir.replace('\\', '/'))
            environment.appendChild(var)
        
        result = dom.toprettyxml().replace("<?xml version=\"1.0\" ?>", "<?xml version=\"1.0\" encoding=\"iso-8859-1\" standalone=\"no\"?>\n")
        result = "\n".join(line for line in result.splitlines() if line.strip())
        
        return result
        
    
    def _get_os_script_call(self):
        if self.conanfile.settings.os =="Windows":
            return "call "
        else:
            return ". "
        
    def _get_os_process_start(self):
        if self.conanfile.settings.os =="Windows":
            return "start /wait "
        else:
            return ""
        
    def _get_os_script_ext(self):
        if self.conanfile.settings.os =="Windows":
            return ".bat"
        else:
            return ".sh"
        
            
    def _get_os_script_params(self):
        if self.conanfile.settings.os =="Windows":
            return " %*"
        else:
            return " $@"
        
    def _get_os_current_script_dir(self):
        if self.conanfile.settings.os =="Windows":
            return "%~dp0"
        else:
            return "$(dirname $(readlink -f $0))/"
    
    def generate_start_script(self, adtf_manifest, globals_xml, project=None, system_xml=None, params=None):
        lines = []
        launcher_call = self._get_os_process_start() +"adtf_launcher " + self._get_os_current_script_dir() + adtf_manifest
        globals_param = " -globals=" + self._get_os_current_script_dir() + globals_xml
        project_param = (" -project=" + project) if project else ""
        config_param = (" -config=" + system_xml) if system_xml else ""
        add_params = " " + (params or "")
        lines.append("@echo off" if self.conanfile.settings.os == "Windows" else "#!/bin/bash")
        lines.append("")
        lines.append("echo calling environment activation")
        lines.append(self._get_os_script_call() + self._get_os_current_script_dir() + "activate" + self._get_os_script_ext())
        line = ""
        # check the used manifest
        if adtf_manifest.endswith("console.manifest") or not project:
            # in console there is no project tree, so we can't load a project file
            # if no project file is given, we can only try to add a config (or empty string)
            line = (launcher_call + globals_param + config_param + add_params + self._get_os_script_params())
        elif adtf_manifest.endswith("debugmon.manifest"):
            # debugmon does not need a project/config and no additional params 
            line = (launcher_call + globals_param + self._get_os_script_params())
        elif project:
            # project is given and not console or debug mon
            line = (launcher_call + globals_param + project_param + add_params + self._get_os_script_params())
        else:
            # should not happen
            self.conanfile.output.error("Don't know what to generate/run.")
        lines.append("echo -------------------- starting ADTF configuration with: --------------------")
        lines.append("echo %s" % line)
        lines.append("echo ---------------------------------------------------------------------------")
        lines.append(line)    
        lines.append("echo calling environment deactivation")
        lines.append(self._get_os_script_call() + self._get_os_current_script_dir() + "deactivate" + self._get_os_script_ext())
        lines.append("")    
        lines.append("@echo on" if self.conanfile.settings.os == "Windows" else "")
        
        return os.linesep.join(lines)

    def generate_layout(self, layout_in):
        with open(layout_in, "r+") as f:
            result = f.read()
        return result
    
    def generate_settings_file(self, settings_in):
        from xml.dom import minidom
        
        content = load(settings_in).replace(u'\n', u'')
        dom = minidom.parseString(content)
        
        folders_group = dom.getElementsByTagName("folder")
        if len(folders_group) == 0:
            # probably error message
            pass
        
        for folders in folders_group:
            if folders.getAttribute("name") == "project_tree":
                subfolder_group = folders.getElementsByTagName("folder")
                for subfolder in subfolder_group:
                    if subfolder.getAttribute("name") == "templates":
                        templates_group = subfolder.getElementsByTagName("templates")
                        for template in templates_group:
                            old_val = template.getAttribute("url")
                            template.setAttribute("url", self.ADTF_bin_dir + "/" + old_val)
                        
                        for dep_name, dep_dir in self.deps_dirs.items():
                            templ_path = dep_dir.replace("\\", "/") + "/bin/templates"
                            if not dep_name == "ADTF" and os.path.exists(templ_path):
                                new_templates = dom.createElement("templates")
                                new_templates.setAttribute("optional", "true")
                                new_templates.setAttribute("url", templ_path)
                                new_templates.setAttribute("name", dep_name)
                                subfolder.appendChild(new_templates)
        
        result = dom.toprettyxml().replace("<?xml version=\"1.0\" ?>", "<?xml version=\"1.0\" encoding=\"iso-8859-1\" standalone=\"no\"?>\n")
        result = "\n".join(line for line in result.splitlines() if line.strip())
        return result
        

    @property
    def content(self):
        import glob
        result = {}     

        projects_dicts = self.ADTF_projects
        # append a None project to get a universal startup script
        projects_dicts.append(None)
        for project_dict in projects_dicts:
            # get all settings from project
            # get start parameter (e.g. -run)
            start_params = (project_dict.get("START_PARAMETER") if project_dict else None)
            # get the project path
            project_path = (project_dict.get("PROJECT_PATH") if project_dict else None)
            # get the system.xml path
            config_path = (project_dict.get("CONFIG_PATH") if project_dict else None)
            # just use the listed manifests
            manifests2use = (project_dict.get("MANIFESTS_USE") if project_dict else None) or []
            # just use the listed globals
            globals2use = (project_dict.get("GLOBALS_USE") if project_dict else None) or []
            
            ###############################
            # 1. get all original ADTF manifest files (probably only the desired one)
            ###############################
            # create a list of all manifests in ADTF bin dir
            manifests_list = []
            # get all manifests
            manifests_search_result = glob.glob(os.path.join(self.ADTF_bin_dir, "*.manifest"))
            if len(manifests2use) > 0:
                # only the listed manifests has to be processed
                for manifest in manifests_search_result:
                    # walk over all manifests
                    if os.path.basename(manifest) in manifests2use:
                        # add manifest to list
                        manifests_list.append(manifest)
            else:
                # add all found manifests to list
                manifests_list = manifests_search_result
            
            # extend the manifest list with custom manifests   
            manifests_list.extend(self.ADTF_custom_manifests)
            
            ###############################
            # 2. get all original ADTF globals files (probably only the desired one)
            ###############################
            # create list of all globals in ADTF bin dir 
            globals_list = []
            # get all globals from ADTF bin dir
            globals_search_result = glob.glob(os.path.join(self.ADTF_bin_dir, "globals*.xml")) 
            if len(globals2use) > 0:
                # only the listed globals has to be processed 
                # first process all globals from ADTF bin dir
                for globals_xml in globals_search_result:
                    # walk over all globals
                    if os.path.basename(globals_xml) in globals2use:
                        # add globals to list if it has to be used
                        globals_list.append(globals_xml)
                # second iterate over all globals to be used and append all globals which are NOT
                # in ADTF bin dir
                for the_globals in globals2use:
                    # the globals in ADTF_bin_dir do not have a parent directory
                    if os.path.dirname(the_globals):
                        if not os.path.exists(the_globals):
                            raise ConanException("The globals file %s can't be found." % the_globals)
                        globals_list.append(the_globals)
            else:
                # add all found globals
                globals_list = globals_search_result
                
            ###############################
            # 4. loop all manifests
            ###############################
            # process manifests to create the start scripts (launcher + manifest == start_script_name)
            for manifest in manifests_list:
                # create the config name if project_dict is set AND it is not the debugmon (which does not need a project)
                config_name = ("_" + os.path.basename(project_path).replace(".prj", "")) if project_path and not manifest.endswith("debugmon.manifest") else ""
                ###############################
                # 5. generate globals xml files
                ###############################
                # process and generate the globals files
                for globals_xml in globals_list:
                    if self.ADTF_bin_dir.replace("\\", "/") not in globals_xml.replace("\\", "/") and not config_name:
                        # skip generation of custom globals if config is not defined
                        continue
                    nameSplit = os.path.basename(globals_xml).split('.')
                    nameSplit[0] = nameSplit[0] + config_name
                    # define the file name
                    name = self.generate_2_dir + "/" + ".".join(nameSplit)
                    # define the content
                    content = self.generate_globals(globals_xml)
                    result[name] = content
                
                nameSplit = os.path.basename(manifest).split(".")
                nameSplit[0] = nameSplit[0] + config_name
                
                # define the file name
                manifest_new_name = os.path.join(self.generate_2_dir, ".".join(nameSplit))
                # define the content
                content = self.generate_manifest(manifest)
                result[manifest_new_name] = content
                
                # try to find matching settings files
                for settings_file in glob.glob(os.path.join(self.ADTF_bin_dir, manifest.replace(".manifest", "*.settings"))):
                    nameSplit = os.path.basename(settings_file).split(".")
                    nameSplit[0] = nameSplit[0] + config_name
                    # create the name
                    name = os.path.join(self.generate_2_dir, ".".join(nameSplit))
                    # create the content (just read the input file into string)
                    content = self.generate_settings_file(settings_file)
                    result[name] = content
                
                # try to find matching layout files 
                for layout in glob.glob(os.path.join(self.ADTF_bin_dir, manifest.replace(".manifest", "*.systemlayout"))):
                    nameSplit = os.path.basename(layout).split(".")
                    nameSplit[0] = nameSplit[0] + config_name
                    # create the name
                    name = os.path.join(self.generate_2_dir, ".".join(nameSplit))
                    # create the content (just read the input file into string)
                    content = self.generate_layout(layout)
                    result[name] = content
                        
                # script name is based on manifest name + config name 
                for the_globals in globals_list:
                    name = os.path.basename(manifest_new_name).replace(".manifest", "") + self._get_os_script_ext()
                    if "console" in manifest and not "console" in the_globals:
                        # skip console script generation if no globals_console.xml in globals list
                        continue
                    elif not "console" in manifest and "console" in the_globals:
                        # skip console script generation if this is globals_console.xml but not matching manifest
                        continue
                    # create the content of the start script
                    globals_basename = os.path.basename(the_globals).replace(".xml", "")
                    globals_gen_path = os.path.join(self.generate_2_dir, globals_basename + config_name + ".xml")
                    content = self.generate_start_script(
                                    manifest_new_name, 
                                    globals_gen_path, 
                                    project_path, 
                                    config_path, 
                                    start_params)
                    result[name] = content
        
        
                    
        
        
        # if there is no virtualenv generator given, it has to be added and called
        # the activate and deactivate scripts are required
        if not "virtualenv" in self.conanfile.generators:
            from conans.client.generators.virtualenv import VirtualEnvGenerator
            veg = VirtualEnvGenerator(self.conanfile)
            result.update(veg.content)
        
        return result
            
                             
                             
class ADTF2GeneratorPackage(ConanFile):
    name = "ADTF2Generator"
    version = "1.1.2"
    url = "https://github.com/AEV/CoRTEX_ADTF2Generator"
    license = "MPL-2.0 - (c) Audi Electronics Venture GmbH 2019"
    description = "%s generates start scripts and all required files for ADTF2 to be able to run an ADTF2 configuration" % name
    
    scm = {
        "type": "git",
        "url": "auto",
        "revision": "auto"
        }
    
    def build(self):
        pass
    
    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []

        