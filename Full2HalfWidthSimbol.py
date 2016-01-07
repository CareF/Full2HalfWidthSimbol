#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: ShowTexdoc.py
# Author:   Lyu Ming <CareF.Lm@gmail.com>

import sublime, sublime_plugin
import re

def replace_in_dict(xin, dicts):
    xout = ""
    for c in xin:
        xout += dicts[c]
    return xout

def replace_simbol(texts):
    s = sublime.load_settings("Full2HalfWidthSimbol.sublime-settings")
    sdict_left = s.get("left")
    sdict_right = s.get("right")
    sdict_right.update(s.get("end"))
    sdict_chara = s.get("character")
    # space formatting
    # if sdict_left:
    #     for item in sdict_left: 
    #         if not sdict_left[item][0].isspace(): 
    #             sdict_left[item] = " " + sdict_left[item]
    # if sdict_right:
    #     for item in sdict_right: 
    #         if not sdict_right[item][-1].isspace(): 
    #             sdict_right[item] += " "
    # if sdict_chara:
    #     for item in sdict_chara: 
    #         if not sdict_chara[item][0].isspace(): 
    #             sdict_chara[item] = " " + sdict_chara[item]
    #         if not sdict_chara[item][-1].isspace(): 
    #             sdict_chara[item] += " "
    pattern_left = re.compile(r' ?(' + '|'.join(sdict_left.keys()) + r')+')
    pattern_right = re.compile(r'(' + '|'.join(sdict_right.keys()) + r')+ ?')
    pattern_chara = re.compile(r'(' + '|'.join(sdict_chara.keys()) + r')+')

    texts = pattern_left.sub(lambda x: 
        " "+replace_in_dict( x.group(), sdict_left), texts)
    texts = pattern_right.sub(lambda x: 
        replace_in_dict( x.group(), sdict_right)+" ", texts)
    texts = pattern_chara.sub(lambda x: 
        " "+replace_in_dict( x.group(), sdict_chara)+" ", texts)

    return texts

class SwitchCommand(sublime_plugin.TextCommand):
    '''Switch full width simbol to half width'''
    def run(self, edit):
        view = self.view
        if view.is_read_only(): 
            sublime.status_message("Full2HalfWidthSimbol: Cannot \
                modify (read only)!")
            return

        region = sublime.Region(0, view.size())
        texts = view.substr(region)
        texts = replace_simbol(texts)
        view.replace(edit, region, texts)
        sublime.status_message("Full2HalfWidthSimbol: Done with whole!")

class SwitchSelectedCommand(sublime_plugin.TextCommand):
    '''Switch full width simbol to half width'''
    def run(self, edit):
        view = self.view
        if view.is_read_only(): 
            sublime.status_message("Full2HalfWidthSimbol: Cannot \
                modify (read only)!")
            return
        for region in view.sel(): 
            texts = view.substr(region)
            texts = replace_simbol(texts)
            view.replace(edit, region, texts)
        sublime.status_message("Full2HalfWidthSimbol: Done with selected!")