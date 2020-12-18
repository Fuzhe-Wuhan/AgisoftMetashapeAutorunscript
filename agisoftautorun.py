'''
@article{Chris,
    author = {Xingye Chris Hu},
    title  = {Agisoft autorun python script},
    year   = {2020},
}
'''

import Metashape
import os
import time
import datetime

#####################################################################路径参数#########################################################################
path_root = "C:/Users/xiaoh/Desktop/agisoftautorun" #根目录
path_photos = path_root+"/Archive 3"         #放图片的路径
path_export = path_root+"/export"        #生成3d模型的路径
path_mask = path_photos+"/IMG_7796.JPG"  #放mask照片的路径
path_obj = path_export+ "/result.obj"    #生成3d模型的名称
path_denseply = path_export+ "/denseply.ply"    #生成密集点云名称
path_log = path_root+"/log"               #放log的路径 
d=datetime.datetime.now()
pylogdate = "/"+str(d.date())+".txt"       #生成log的名称
######################################################################################################################################################

####################################################################摄影测量参数#######################################################################
#load image 载入图片
ifmask = False          #是否有mask遮罩
masktolerance = 19      #mask遮罩的程度，越大删除的部分越多

#match image 匹配图片
accuracy = 8             #0 Highest, 1 High, 2 Medium, 4 Low, 8 Lowest

#build depthmap and dense point cloud 建立深度图以及建立密集点云
dmquality = 16           #1 Ultra, 2 High, 4 Medium, 8 Low, 16 Lowest

#Export PLY
ifexportply = False

#smooth mesh
ifsmoothmesh = True
smoothstrength = 3.0

######################################################################################################################################################


def diff_time(t2, t1):
    total = str(round(t2-t1, 1))+" sec"
    return total

def checkcreatefolder(path_folder):
    if os.path.exists(path_folder):
        return(1)
    else:
        try:
            os.mkdir(path_folder)
            with open(path_log+pylogdate, 'a') as p:
                p.write("created "+path_folder+"\n")
        except Exception as e:
            os.makedirs(path_folder)
            with open(path_log+pylogdate, 'a') as p:
                p.write("created "+path_folder+"\n")

def loadimage(chunk,ifmask,masktolerance):
    try:
        timeA = time.time()
        # loading images
        image_list = os.listdir(path_photos)
        photo_list = list()
        for photo in image_list:
            if photo.rsplit(".", 1)[1].lower() in ["jpg", "jpeg", "tif", "tiff"]:
                photo_list.append("/".join([path_photos, photo]))
        chunk.addPhotos(photo_list)
        if ifmask:
            chunk.importMasks(path=path_mask, source = Metashape.MaskSourceBackground, operation=Metashape.MaskOperationReplacement,tolerance=masktolerance)
        timeB=time.time()
        with open(path_log+pylogdate, 'a') as p:
            p.write("load image: "+diff_time(timeB,timeA)+"\n")
    except:
        with open(path_log+pylogdate, 'a') as p:
            p.write("unable to load image\n")

def matchimage(chunk,accuracy,ifmask):
    try:
        timeA = time.time()
        chunk.matchPhotos(downscale=accuracy, generic_preselection=True, reference_preselection=False,filter_mask = ifmask, guided_matching=True,subdivide_task=True)
        chunk.alignCameras(subdivide_task=True)
        timeB=time.time()
        with open(path_log+pylogdate, 'a') as p:
            p.write("match photo & align camera: "+diff_time(timeB,timeA)+"\n")
    except:
        with open(path_log+pylogdate, 'a') as p:
            p.write("unable to match image\n")

def depthmap_densecloud(chunk,dmquality):
    try:
        timeA = time.time()
        chunk.buildDepthMaps(downscale=dmquality, filter_mode=Metashape.MildFiltering,subdivide_task=True)
        chunk.buildDenseCloud(subdivide_task=True)
        timeB=time.time()
        with open(path_log+pylogdate, 'a') as p:
            p.write("build depthmap & generate dense pointcloud: "+diff_time(timeB,timeA)+"\n")
    except:
        with open(path_log+pylogdate, 'a') as p:
            p.write("unable to build depthmap or generate dense pointcloud\n")

def exportply(chunk):
    try:
        timeA = time.time()
        chunk.exportPoints(path=path_denseply,source_data=Metashape.DenseCloudData,format=Metashape.PointsFormatPLY)
        timeB=time.time()
        with open(path_log+pylogdate, 'a') as p:
            p.write("export dense cloud: "+diff_time(timeB,timeA)+"\n")
    except:
        with open(path_log+pylogdate, 'a') as p:
            p.write("unable to export densed point cloud\n")

def createmesh(chunk):
    try:
        timeA = time.time()
        chunk.buildModel(surface_type=Metashape.Arbitrary, interpolation=Metashape.EnabledInterpolation)
        timeB = time.time()
        with open(path_log+pylogdate, 'a') as p:
            p.write("create mesh: "+diff_time(timeB,timeA)+"\n")
    except:
        with open(path_log+pylogdate, 'a') as p:
            p.write("unable to createmesh\n")

def smoothmesh(chunk,smoothstrength):
    try:
        timeA = time.time()
        chunk.smoothModel(strength=smoothstrength, apply_to_selection=False, fix_borders=False) 
        timeB = time.time()
        with open(path_log+pylogdate, 'a') as p:
            p.write("smooth mesh: "+diff_time(timeB,timeA)+"\n")
    except:
        with open(path_log+pylogdate, 'a') as p:
            p.write("unable to smooth mesh\n")

def createtexture(chunk):
    try:
        timeA = time.time()
        chunk.buildUV(mapping_mode=Metashape.GenericMapping)
        chunk.buildTexture(blending_mode=Metashape.MosaicBlending, texture_size=4096,fill_holes=True,ghosting_filter=True)
        timeB = time.time()
        with open(path_log+pylogdate, 'a') as p:
            p.write("build texture: "+diff_time(timeB,timeA)+"\n")
    except:
        with open(path_log+pylogdate, 'a') as p:
            p.write("unable to build texture\n")

def exportobj(chunk):
    try:
        timeA = time.time()
        chunk.exportModel(path = path_obj,texture_format=Metashape.ImageFormatJPEG,save_texture=True,format = Metashape.ModelFormatOBJ)
        timeB = time.time()
        with open(path_log+pylogdate, 'a') as p:
            p.write("export model: "+diff_time(timeB,timeA)+"\n")
    except:
        with open(path_log+pylogdate, 'a') as p:
            p.write("unable to export obj model\n")

def main():
    checkcreatefolder(path_log)
    
    with open(path_log+pylogdate, 'a') as p:
        p.write("******************************************************************************************\n")
        p.write(str(datetime.datetime.now())+"\n")
        p.write("Processing start\n")

    timer1=time.time()

    doc = Metashape.Document()
    doc.save(path = path_root+"/newproject.psx")   #保存psx，项目文件
    doc.read_only = False

    chunk = doc.addChunk()
    chunk.label = 'New project'
    

    # STEP 1: Load Photos
    loadimage(chunk,ifmask,masktolerance)

    # STEP 2: Align Photos and Camera
    matchimage(chunk,accuracy,ifmask)

    # STEP 3: Build DepthMaps
    depthmap_densecloud(chunk,dmquality)

    # STEP 3.5: Export Densed PLY
    if ifexportply:
        exportply(chunk)
    
    # STEP 4: Build Model
    createmesh(chunk)

    # STEP 4.5: Smooth Mesh
    if ifsmoothmesh:
        smoothmesh(chunk,smoothstrength)

    # STEP 5: Build Texture
    createtexture(chunk)

    # STEP 6: Export Obj
    exportobj(chunk)

    timer2=time.time()
    
    with open(path_log+pylogdate, 'a') as p:
        p.write("total time: "+diff_time(timer2,timer1)+"\n")
        p.write("Processing complete\n")
        p.write("******************************************************************************************")
    doc.save()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        checkcreatefolder(path_log)
        with open(path_log+pylogdate, 'a') as p:
            p.write("==========================================================================================================\n")
            p.write(str(datetime.datetime.now())+"\n")
            p.write("Error\n")
            p.write(str(e)+"\n")
            p.write("==========================================================================================================\n")
