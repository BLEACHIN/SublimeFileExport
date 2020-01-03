#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# 可调起控制台，输入view.run_command("open_folder")进行调试

'Main'

__author__ = 'Bleachin'

import sublime
import sublime_plugin

import os
import os.path
import shutil
import time
import subprocess

from .Bleachin_utils import *

# 自定义错误
class MyError(Exception): pass

class BleachinBashCommand(sublime_plugin.WindowCommand):
    def run(self, paths=None, isHung=False):            
        dir = get_focused_dir_or_file(paths)

        settings = sublime.load_settings('Bleachin.sublime-settings')
        cmd_path = settings.get('cmd_path')

        if not os.path.isfile(cmd_path):
            sublime.error_message(''.join(['can\'t find cmd.exe (cmd),',
                ' please config setting file', '\n   --sublime-Bleachin']))
            raise MyError("未找到该目录，请重新配置Settings - User文件")

        if os.path.isfile(dir):
            command = 'explorer /select,%s ' % (dir) # 打开文件夹，并聚焦到文件
        else:
            command = 'explorer %s ' % (dir) 
        
        subprocess.Popen(command)

# 打开文件夹资源
class OpenFolderCommand(BleachinBashCommand):
    def run(self, paths=None):
        BleachinBashCommand.run(self, paths)

# 导出文件到桌面，类似svn export，包含目录
class ExportFileCommand(sublime_plugin.WindowCommand):
    def run(self, paths=None, isHung=False):            
        dir = get_focused_dir_or_file(paths) # 文件的绝对路径，包括文件名
        print(get_current_dir(self.window)) 
        print(dir) 

        if not os.path.isfile(dir):
            sublime.error_message(''.join(['not a file']))
            raise MyError("请选择一个文件")

        settings = sublime.load_settings('Bleachin.sublime-settings')
        cmd_path = settings.get('cmd_path')
        desktop_path = settings.get('desktop_path') # 导出的目标路径
        top_path = get_current_dir(self.window) # 获取顶级目录路径

        if not os.path.isfile(cmd_path):
            sublime.error_message(''.join(['can\'t find cmd.exe (cmd),',
                ' please config setting file', '\nSettings - User']))
            raise MyError("未找到cmd.exe文件，请重新配置Settings - User文件")

        if not os.path.isdir(desktop_path):
            sublime.error_message(''.join(['can\'t find this dir,',
                ' please config setting file', '\nSettings - User']))
            raise MyError("未找到该目录，请重新配置Settings - User文件")

        top_path_last = os.path.basename(top_path) # 获取顶级目录路径的最后一个部分
        file_path = os.path.dirname(dir) # 获取文件路径不包括文件名
        tmp_path = file_path.replace(top_path, '') # 文件路径去掉顶级目录部分
        target_path = desktop_path + "\\" + top_path_last + tmp_path # 拼接成目标路径
        print(top_path_last)
        print(file_path)
        print(tmp_path)
        print(target_path)

        # os.mkdir(target_path) # 创建目录，如果该目录已经存在，则引发FileExistsError。
        os.makedirs(target_path, mode=0o777, exist_ok=True) # 递归创建目录，类似mkdir -p
        shutil.copy(dir, target_path) # 复制文件到目标目录，原文件存在则覆盖

        # sublime.message_dialog('Success')
        sublime.status_message('Success') # 最下方的status bar显示成功信息

# 导出文件到桌面，类似svn export，只导出文件
class ExportOnlyFileCommand(sublime_plugin.WindowCommand):
    def run(self, paths=None, isHung=False):            
        dir = get_focused_dir_or_file(paths) # 文件的绝对路径，包括文件名
        print(get_current_dir(self.window)) 
        print(dir) 

        if not os.path.isfile(dir):
            sublime.error_message(''.join(['not a file']))
            raise MyError("请选择一个文件")

        settings = sublime.load_settings('Bleachin.sublime-settings')
        cmd_path = settings.get('cmd_path')
        desktop_path = settings.get('desktop_path') # 导出的目标路径
        top_path = get_current_dir(self.window) # 获取顶级目录路径

        if not os.path.isfile(cmd_path):
            sublime.error_message(''.join(['can\'t find cmd.exe (cmd),',
                ' please config setting file', '\nSettings - User']))
            raise MyError("未找到cmd.exe文件，请重新配置Settings - User文件")

        if not os.path.isdir(desktop_path):
            sublime.error_message(''.join(['can\'t find this dir,',
                ' please config setting file', '\nSettings - User']))
            raise MyError("未找到该目录，请重新配置Settings - User文件")

        print(desktop_path)

        shutil.copy(dir, desktop_path) # 复制文件到目标目录，原文件存在则覆盖

        # sublime.message_dialog('Success')
        sublime.status_message('Success') # 最下方的status bar显示成功信息