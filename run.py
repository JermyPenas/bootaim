from logic .config_watcher import Config #line:1
cfg =Config ()#line:2
from logic .keyboard import *#line:3
from logic .capture import *#line:4
from logic .mouse import MouseThread #line:5
from ultralytics import YOLO #line:7
import math #line:8
import torch #line:9
import cv2 #line:10
import time #line:11
import win32api ,win32con ,win32gui #line:12
class Targets :#line:14
    def __init__ (OO0O0O00OOOOO0OO0 ,OOOOO0OOO00O0OO00 ,O00OO0O00O0O0O00O ,OO00000OO00O0O0OO ,O0OO000O0OOO0OO00 ,OO00OOO0000000O00 ):#line:15
        OO0O0O00OOOOO0OO0 .mouse_x =OOOOO0OOO00O0OO00 -frames .screen_x_center #line:16
        OO0O0O00OOOOO0OO0 .mouse_y =(O00OO0O00O0O0O00O -frames .screen_y_center )if OO00OOO0000000O00 ==7 else (O00OO0O00O0O0O00O -frames .screen_y_center -cfg .body_y_offset *O0OO000O0OOO0OO00 )#line:17
        OO0O0O00OOOOO0OO0 .distance =math .sqrt ((OOOOO0OOO00O0OO00 -frames .screen_x_center )**2 +(O00OO0O00O0O0O00O -frames .screen_y_center )**2 )#line:18
        OO0O0O00OOOOO0OO0 .x =OOOOO0OOO00O0OO00 #line:19
        OO0O0O00OOOOO0OO0 .y =O00OO0O00O0O0O00O #line:20
        OO0O0O00OOOOO0OO0 .w =OO00000OO00O0O0OO #line:21
        OO0O0O00OOOOO0OO0 .h =O0OO000O0OOO0OO00 #line:22
        OO0O0O00OOOOO0OO0 .cls =OO00OOO0000000O00 #line:23
@torch .no_grad ()#line:25
def init ():#line:26
    if cfg .show_window and cfg .show_fps :#line:27
        O0OOOOO00OO0O00OO =0 #line:28
        O000O00OO000OOOO0 =0 #line:29
    try :#line:30
        OOOOOOOO00O00OO0O =YOLO ('models/{}'.format (cfg .AI_model_path ),task ='detect')#line:31
    except Exception as O000O00OOO00O0OO0 :#line:32
        print (O000O00OOO00O0OO0 )#line:33
        quit (0 )#line:34
    if '.pt'in cfg .AI_model_path :#line:36
        print ('PT Model loaded.\nYou are using .pt model, exporting the model to the .engine format will give a huge increase in performance!')#line:37
    if '.onnx'in cfg .AI_model_path :#line:38
        print ('Onnx CPU loaded.')#line:39
    if '.engine'in cfg .AI_model_path :#line:40
        print ('Engine loaded')#line:41
    print ('\033[32mAimbot is started. Enjoy!\033[0m\n[\033[33m'+cfg .hotkey_targeting +'\033[0m] - Aiming at the target\n[\033[33m'+cfg .hotkey_exit +'\033[0m] - EXIT\n[\033[33m'+cfg .hotkey_pause +'\033[0m] - PAUSE AIM\n[\033[33m'+cfg .hotkey_reload_config +'\033[0m] - Reload config')#line:43
    if cfg .show_window :#line:45
        print ('An open debug window can affect performance.')#line:46
        cv2 .namedWindow (cfg .debug_window_name )#line:47
        if cfg .debug_window_always_on_top :#line:48
            OO0OO0O000O0OO0O0 =win32gui .FindWindow (None ,cfg .debug_window_name )#line:49
            win32gui .SetWindowPos (OO0OO0O000O0OO0O0 ,win32con .HWND_TOPMOST ,100 ,100 ,200 ,200 ,0 )#line:50
    O0O0000OOO0O0O00O =[]#line:52
    if cfg .hideout_targets :#line:53
        O0O0000OOO0O0O00O =[0 ,1 ,5 ,6 ,7 ]#line:54
    if cfg .hideout_targets ==False :#line:55
        O0O0000OOO0O0O00O =[0 ,1 ,7 ]#line:56
    OOOOOO00OOO0O0000 =0 #line:58
    O000000000OO0000O =[]#line:59
    while True :#line:60
        O00O0OO0000OOOO0O =win32api .GetKeyState (Keyboard .KeyCodes .get (cfg .hotkey_pause ))#line:61
        OOO0OO00O0O0O0OO0 =win32api .GetKeyState (Keyboard .KeyCodes .get (cfg .hotkey_reload_config ))#line:63
        if OOO0OO00O0O0O0OO0 !=OOOOOO00OOO0O0000 :#line:64
            if OOO0OO00O0O0O0OO0 ==1 or OOO0OO00O0O0O0OO0 ==0 :#line:65
                cfg .Read (verbose =True )#line:66
                frames .reload_capture ()#line:67
                mouse_worker .Update_settings ()#line:68
        OOOOOO00OOO0O0000 =OOO0OO00O0O0O0OO0 #line:69
        O0O00OOO00OO0000O =frames .get_new_frame ()#line:71
        OO0O0O0OO0O00OO0O =OOOOOOOO00O00OO0O .predict (source =O0O00OOO00OO0000O ,stream =True ,cfg ='logic/game.yaml',imgsz =cfg .AI_image_size ,stream_buffer =False ,visualize =False ,augment =True ,agnostic_nms =False ,save =False ,conf =cfg .AI_conf ,iou =cfg .AI_iou ,device =cfg .AI_device ,half =False ,max_det =cfg .AI_max_det ,vid_stride =False ,classes =O0O0000OOO0O0O00O ,verbose =False ,show_boxes =False ,show_labels =False ,show_conf =False ,show =False )#line:93
        if cfg .show_window :#line:95
            OO00O0O00OO00O000 =int (cfg .detection_window_height *cfg .debug_window_scale_percent /100 )#line:96
            OOO0O000O00O0000O =int (cfg .detection_window_width *cfg .debug_window_scale_percent /100 )#line:97
            O000OOO0O0OOO00OO =(OOO0O000O00O0000O ,OO00O0O00OO00O000 )#line:98
            O000000O0O00O0O00 =O0O00OOO00OO0000O #line:100
        for OOO000O0OO0OOOO00 in OO0O0O0OO0O00OO0O :#line:102
            if cfg .show_window and cfg .show_speed ==True :#line:103
                O000000O0O00O0O00 =speed (O000000O0O00O0O00 ,OOO000O0OO0OOOO00 .speed ['preprocess'],OOO000O0OO0OOOO00 .speed ['inference'],OOO000O0OO0OOOO00 .speed ['postprocess'])#line:104
            if len (OOO000O0OO0OOOO00 .boxes ):#line:106
                if O00O0OO0000OOOO0O ==0 :#line:107
                    for OO0O0OOOO00O00000 in OOO000O0OO0OOOO00 .boxes :#line:108
                        O0OOO00OOOOOO0OO0 =int (OO0O0OOOO00O00000 .cls .item ())#line:109
                        if not cfg .disable_headshot :#line:110
                            O000000000OO0000O .append (Targets (*OO0O0OOOO00O00000 .xywh [0 ],O0OOO00OOOOOO0OO0 ))#line:111
                        elif O0OOO00OOOOOO0OO0 in (0 ,1 ,5 ,6 ):#line:112
                            O000000000OO0000O .append (Targets (*OO0O0OOOO00O00000 .xywh [0 ],O0OOO00OOOOOO0OO0 ))#line:113
                    if not cfg .disable_headshot :#line:115
                        O000000000OO0000O .sort (key =lambda O0OOO0OOO0OOOO0OO :(O0OOO0OOO0OOOO0OO .cls !=7 ,O0OOO0OOO0OOOO0OO .distance ))#line:116
                    else :#line:117
                        O000000000OO0000O .sort (key =lambda OO00OO00O00OO0000 :OO00OO00O00OO0000 .distance ,reverse =False )#line:118
                    try :#line:119
                        O0000OOO0OO0OO000 =O000000000OO0000O [0 ]#line:120
                        mouse_worker .queue .put ((O0000OOO0OO0OO000 .mouse_x ,O0000OOO0OO0OO000 .mouse_y ,O0000OOO0OO0OO000 .x ,O0000OOO0OO0OO000 .y ,O0000OOO0OO0OO000 .w ,O0000OOO0OO0OO000 .h ,O0000OOO0OO0OO000 .distance ))#line:128
                        if cfg .show_window and cfg .show_target_line :#line:129
                            draw_target_line (annotated_frame =O000000O0O00O0O00 ,screen_x_center =cfg .detection_window_width /2 ,screen_y_center =cfg .detection_window_height /2 ,target_x =O0000OOO0OO0OO000 .mouse_x +frames .screen_x_center ,target_y =O0000OOO0OO0OO000 .mouse_y +frames .screen_y_center +cfg .body_y_offset /O0000OOO0OO0OO000 .h )#line:130
                    except IndexError :#line:131
                        mouse_worker .queue .put (None )#line:132
                        O000000000OO0000O .clear ()#line:133
                    O000000000OO0000O .clear ()#line:134
                else :pass #line:135
                if cfg .show_window and cfg .show_boxes :#line:137
                    draw_helpers (annotated_frame =O000000O0O00O0O00 ,boxes =OOO000O0OO0OOOO00 .boxes )#line:138
            else :#line:139
                mouse_worker .queue .put (None )#line:140
        if cfg .show_window and cfg .show_fps :#line:142
            O000O00OO000OOOO0 =time .time ()#line:143
            OO0O0000O0OOO00OO =1 /(O000O00OO000OOOO0 -O0OOOOO00OO0O00OO )#line:144
            O0OOOOO00OO0O00OO =O000O00OO000OOOO0 #line:145
            if cfg .show_speed :#line:147
                cv2 .putText (O000000O0O00O0O00 ,'FPS: {0}'.format (str (int (OO0O0000O0OOO00OO ))),(10 ,100 ),cv2 .FONT_HERSHEY_SIMPLEX ,0.6 ,(0 ,255 ,0 ),1 ,cv2 .LINE_AA )#line:148
            else :#line:149
                cv2 .putText (O000000O0O00O0O00 ,'FPS: {0}'.format (str (int (OO0O0000O0OOO00OO ))),(10 ,20 ),cv2 .FONT_HERSHEY_SIMPLEX ,0.6 ,(0 ,255 ,0 ),1 ,cv2 .LINE_AA )#line:150
        if win32api .GetAsyncKeyState (Keyboard .KeyCodes .get (cfg .hotkey_exit ))&0xFF :#line:152
            if cfg .show_window :#line:153
                cv2 .destroyWindow (cfg .debug_window_name )#line:154
            frames .Quit ()#line:155
            break #line:156
        if cfg .show_window :#line:158
            try :#line:159
                cv2 .resizeWindow (cfg .debug_window_name ,O000OOO0O0OOO00OO )#line:160
            except :exit (0 )#line:161
            O0O0OOO00O0000O0O =cv2 .resize (O000000O0O00O0O00 ,O000OOO0O0OOO00OO ,cv2 .INTER_NEAREST )#line:162
            cv2 .imshow (cfg .debug_window_name ,O0O0OOO00O0000O0O )#line:163
            if cv2 .waitKey (1 )&0xFF ==ord ('q'):#line:164
                break #line:165
if __name__ =="__main__":#line:167
    frames =Capture ()#line:168
    mouse_worker =MouseThread ()#line:169
    init ()