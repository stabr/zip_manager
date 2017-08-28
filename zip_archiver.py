'''

description: zip archiver class to zip project files for outsource

author: Dmitry Stabrov
mailto: fx@dimastabrov.com
'''

import os
import sys
import re
import shutil
import zipfile

from PySide.QtCore import *
from PySide.QtGui import *

import setup
prj_root = setup.config('project_root')

class ZipArchiver(QObject):
    message = Signal(str)
    progres = Signal(int)
    finished = Signal()
    def __init__(self, file, override):
        super(ZipArchiver, self).__init__()
        # values
        self.override = override
        self.file = file.replace('\\','/')
        self.root = '/'.join([prj_root, file[len(prj_root)+1:].partition('/')[0]])

    def send_message(self, val, msg):
        if val > 0:
            self.progres.emit(val)
        if msg:
            self.message.emit(msg)

    def remove_duplicates(self, itm_lst):
        # remove the possible duplicated file names
        # files = set(files); files = list(files) - this way can change list order
        non_dup_lst = []
        for itm in itm_lst:
            if not itm in non_dup_lst:
                non_dup_lst.append(itm)
        return non_dup_lst
    
    def get_scene_paths(self, maya_scene, pth=[], errors=[]):
        # maya_scene must be a string
        if not os.path.exists(maya_scene):
            return
        with open(maya_scene) as fp:
            for ln in fp:
                src = re.findall('(\"\S+\/\S+\.[a-z]{2,4})', ln)
                if src:
                    src = src[0][1:]
                    if src in pth or src in errors:
                        continue
                    if  'Model' in src or '/surf/' in src or '<udim>' in src.lower():
                        continue
                    if not os.path.exists(src):
                        errors.append(('notexists', src))
                        continue
                    if '/outsource/' in src:
                        errors.append(('unexpected', src))
                        continue
                    pth.append(src)
                    if 'tex/low' in src.replace('\\','/'):
                            for fl in os.listdir(os.path.dirname(src)):
                                if fl.split('.')[0] == os.path.basename(src).split('.')[0]:
                                    low_src = os.path.join(os.path.dirname(src), fl)
                                    pth.append(low_src)
                    if src.endswith('.ma'):
                        self.get_scene_paths(src, pth, errors)
        return self.remove_duplicates(pth), self.remove_duplicates(errors)

    def copy_file(self, src, trg):
        # copy files to outcoming dir

        if 'win32' == sys.platform:
            src = src.replace('/', '\\')
            trg = trg.replace('/', '\\')
        else:
            src = src.replace('\\','/')[src.index(prj_root):]
            trg = trg.replace('\\','/')[trg.index(prj_root):]

        the_same = src == trg
        src_exists = os.path.exists(src)
        trg_exists = os.path.exists(trg)

        if not 'assets' in src or not 'amg_library' in src:
            trg_exists = False
        if self.override:
            trg_exists = False
            # the_same = False

        if not the_same and src_exists and not trg_exists:
            trg_dir = os.path.dirname(trg)
            if not os.path.exists(trg_dir):
                os.makedirs(trg_dir)
            try:
                shutil.copy2(src, trg)
                return True
            except Exception, e:
                self.message.emit('ERROR::copying from\n>> %s\n>> to:\n>> %s\n>> exception: %s'%(src, trg, e))
                return False
        else:
            return False
    
    def get_paths(self, src):
        src = '/'+src.replace('//','/') # to avoid "//" in the middle of the maya relative paths
        if 'global_library' in src:
            trg = '%s/outsource/amg_library/global_library%s' % (self.root, src.split('global_library')[-1].replace('\\','/'))
            src = src.replace('common_library','amg_library')
        else:
            src = self.root + src[len(self.root):] # to avoid Sensitive-to-Case conflict in project_folder name
            trg = '%s/outsource%s'% (self.root, src[len(self.root):])
        return src, trg

    def change_scene_paths(self, trg_maya):
        with open(trg_maya,'r+') as f:
            for ln in f.readlines():
                src = re.findall('(\"\S+\/\S+\.[a-z]{2,4})', ln)
                if src:
                    src = src[0][1:]
                    src, trg = self.get_paths(src)
                    relative_path = trg.split('outsource/')[-1]
                    ln = ln.replace(src, relative_path)
                f.write(ln)
    
    def zip_asset(self, paths):
        # paths[-1] - "targeted" self.file
        dirr, name = paths[-1].rsplit('/', 5)[:2]
        aset_zip_name = dirr+'/%s.zip'%name
        as_zip = zipfile.ZipFile(aset_zip_name, 'w', zipfile.ZIP_DEFLATED)

        for i, file in enumerate(paths):
                rel_path = file.split('outsource/')[-1]
                try:
                    as_zip.write(file, rel_path)
                except Exception, e:
                    self.message.emit('ERROR::zip exception - %s'%e)
                self.progres.emit(50+i*50/len(paths))
        as_zip.close()

    def zip_shot(self, paths):
        dirr, name =  os.path.split(paths[-1])
        name = re.findall('(EP\d+\-sh-\d{4})', name)[0]
        ep = re.findall('(EP\d+)', dirr)[0]
        dirr = dirr.split(ep+'-')[0]
    
        shot_zip_name = dirr+'%s.zip'%name
        aset_zip_name = dirr+'%s_assets.zip'%name

        as_zip=zipfile.ZipFile(aset_zip_name, 'w', zipfile.ZIP_DEFLATED)
        sh_zip=zipfile.ZipFile(shot_zip_name, 'w', zipfile.ZIP_DEFLATED)

        for i, file in enumerate(paths):
                # print '>> zip - %s'%file
                rel_path = file.split('outsource/')[-1]
                try:
                    if '-sh-' in file:
                        sh_zip.write(file, rel_path)
                    else:
                        as_zip.write(file, rel_path)
                        self.message.emit('MESSAGE::ZIP - %s'%file)
                except Exception, e:
                    self.message.emit('ERROR::zip exception - %s'%e)
                self.progres.emit(50+i*50/len(paths))

        as_zip.close()
        sh_zip.close()

    def zip_scene(self, paths):
        self.send_message(50, '\nMESSAGE::%s files to zip..   '%len(paths))
        if '/assets/' in self.file:
            self.zip_asset(paths)
        else:
            self.zip_shot(paths)
        self.send_message(99, 'MESSAGE::The Scene Has Been Zipped.')

    def pack_scene(self):
        if not os.path.exists(self.file):
                    self.message.emit('ERROR::Given path does not exist:\n%s'%self.file)
                    self.finished.emit()
                    return
        self.send_message(1, '\nMESSAGE::Packing:  %s    \n'%self.file)
        paths, errors = self.get_scene_paths(self.file, []) # initial value of paths = [] given as a second argument
        self.progres.emit(3)
        if len(errors)>0:
            self.message.emit( ''.join(('ERROR::%s - %s\n'%(e[0],e[1]) for e in errors)) )
            # self.finished.emit()
            # return

        paths.append(self.file)
        self.progres.emit(5)
        to_zip = []
        for i, src in enumerate(paths):
            src, trg = self.get_paths(src) # to avoid Sensitive-to-Case conflict in project_folder name src also can be modified
            self.copy_file(src,trg)
            if trg.endswith('.ma'):
                    self.change_scene_paths(trg)
            if os.path.exists(trg):
                to_zip.append(trg)
            self.progres.emit(5+i*45/len(paths))

        to_zip =['%s/outsource/workspace.mel'%self.root]+to_zip
        self.zip_scene(to_zip)
        self.progres.emit(100)
        self.finished.emit()