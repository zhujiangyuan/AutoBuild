g_default_build_root_path = 'I:\\Application_defualt\\dev\\src'
g_full_work_path = ''
g_project_order_list = []
g_project_order_file_name = '\\auto_build_project_order.txt'
g_Build_Configuration = '\\TwsBuildConfigurations'

g_hg_command_pull = 'hg pull'
g_hg_command_update = 'hg update'
g_gradlew_fAD = 'gradlew.bat fAD'
g_gradlew_cR = 'gradlew.bat cR'
g_gradlew_bR = 'gradlew.bat bR'

import sys
import os
import datetime
import AutoBuildHelper

# Get input path
arg_num = len(sys.argv)
if(1 == arg_num):
   g_full_work_path = g_default_build_root_path
else:
   g_full_work_path = sys.argv[1]

# Read project order from file
project_order_file_path = os.getcwd() + g_project_order_file_name
openfile= open(project_order_file_path)
while True:
    line = openfile.readline()
    if len(line) == 0:
        break
    else:
        g_project_order_list.append(line.strip('\n'))
openfile.close()

#Get all projects

class Poject:
    ''' This class represents each projec. '''
    def __init__ (self, project_name, project_full_path):
        self.project_name = project_name
        self.project_full_path = project_full_path

g_unordered_project_list = []

# dirpath, dirnames, filenames = os.walk(g_full_work_path)
file_list = os.listdir(g_full_work_path)
folder_list = []
for each_file in file_list:
    file_path = os.path.join(g_full_work_path, each_file)
    if(os.path.isdir(file_path)):
        each_project = Poject (each_file, file_path)
        g_unordered_project_list.append(each_project)

#Sort project
g_ordered_project_list =[]
for project_name in g_project_order_list:
    for project_need_complie in g_unordered_project_list:
        if(project_need_complie.project_name == project_name) :
           g_ordered_project_list.append(project_need_complie)
 
# Update Source code
for project in g_ordered_project_list:
    os.chdir(project.project_full_path)
    AutoBuildHelper.RunCommand(g_hg_command_pull)
    AutoBuildHelper.RunCommand(g_hg_command_update)
    
# Run gradle command
for project in g_ordered_project_list:
    os.chdir(project.project_full_path)
    if (False == AutoBuildHelper.ReNameFolderName(project.project_full_path + g_Build_Configuration)):
        print('Failed to Rename TwsBuildConfiguration:' + ' for '+ project.project_name)
        break
    if(False == AutoBuildHelper.RunCommandWithLog(g_gradlew_fAD)):
        print('Failed to Run Command:' + g_gradlew_fAD + ' for '+ project.project_name)
        break
    if(False == AutoBuildHelper.RunCommandWithLog(g_gradlew_cR)):
        print('Failed to Run Command:' +  g_gradlew_fAD + ' for '+ project.project_name)
        break
    if(False == AutoBuildHelper.RunCommandWithLog(g_gradlew_bR)):
        print('Failed to Run Command:' + g_gradlew_fAD + ' for '+ project.project_name)
        break

print('Finsihed!')