#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'function tools'

__author__ = 'Bleachin'

import os
import time
import sublime

import subprocess

def get_path(paths):
    path = None
    if paths:
        path = '*'.join(paths)
    else:
        view = sublime.active_window().active_view()
        path = view.file_name() if view else None

    return path

# 获取鼠标所指的目录或文件
def get_focused_dir_or_file(paths):
    if paths is not None:
        for index, path in enumerate(paths):
          if "${PROJECT_PATH}" in path:
              project_data  = sublime.active_window().project_data()
              project_folder = project_data['folders'][0]['path']
              path = path.replace("${PROJECT_PATH}", project_folder);
              paths[index] = path   
    dir = get_path(paths)

    return dir

# 获取当前工作目录的顶级文件夹的路径
def get_current_dir(window):
    folders = window.folders()
    if len(folders) == 1:
        return folders[0]
    else:
        active_view = window.active_view()
        active_file_name = active_view.file_name() if active_view else None
        if not active_file_name:
            return folders[0] if len(folders) else os.path.expanduser("~")
        for folder in folders:
            if active_file_name.startswith(folder):
                return folder
        return os.path.dirname(active_file_name)