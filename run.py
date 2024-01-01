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
    def __init__ (O00OO000O0O0O00O0 ,O00O0OOOO00O0OO00 ,O0OO00OO0OOOO00O0 ,OOO0OOOO0O0O0OOO0 ,O000O000O000OOOO0 ,O0O00OOO00OOOOOOO ):#line:15
        O00OO000O0O0O00O0 .mouse_x =O00O0OOOO00O0OO00 -frames .screen_x_center #line:16
        O00OO000O0O0O00O0 .mouse_y =(O0OO00OO0OOOO00O0 -frames .screen_y_center )if O0O00OOO00OOOOOOO ==7 else (O0OO00OO0OOOO00O0 -frames .screen_y_center -cfg .body_y_offset *O000O000O000OOOO0 )#line:17
        O00OO000O0O0O00O0 .distance =math .sqrt ((O00O0OOOO00O0OO00 -frames .screen_x_center )**2 +(O0OO00OO0OOOO00O0 -frames .screen_y_center )**2 )#line:18
        O00OO000O0O0O00O0 .x =O00O0OOOO00O0OO00 #line:19
        O00OO000O0O0O00O0 .y =O0OO00OO0OOOO00O0 #line:20
        O00OO000O0O0O00O0 .w =OOO0OOOO0O0O0OOO0 #line:21
        O00OO000O0O0O00O0 .h =O000O000O000OOOO0 #line:22
        O00OO000O0O0O00O0 .cls =O0O00OOO00OOOOOOO #line:23
@torch .no_grad ()#line:25
def init ():#line:26
    if cfg .show_window and cfg .show_fps :#line:27
        OO0OO00000OOOO00O =0 #line:28
        OO0OO0OOOOOOOO00O =0 #line:29
    try :#line:30
        OO00OOOOOO000OO00 =YOLO ('models/{}'.format (cfg .AI_model_path ),task ='detect')#line:31
    except Exception as O0O0O000O00OOOOOO :#line:32
        print (O0O0O000O00OOOOOO )#line:33
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
            O0OOO000OOOO00O0O =win32gui .FindWindow (None ,cfg .debug_window_name )#line:49
            win32gui .SetWindowPos (O0OOO000OOOO00O0O ,win32con .HWND_TOPMOST ,100 ,100 ,200 ,200 ,0 )#line:50
    OO00OO000O0O000OO =[]#line:52
    if cfg .hideout_targets :#line:53
        OO00OO000O0O000OO =[0 ,1 ,5 ,6 ,7 ]#line:54
    if cfg .hideout_targets ==False :#line:55
        OO00OO000O0O000OO =[0 ,1 ,7 ]#line:56
    OO00O0OOOO0O00O0O =0 #line:58
    OOOO000000OO00O0O =[]#line:59
    while True :#line:60
        OOOO0O000O00OOO0O =win32api .GetKeyState (Keyboard .KeyCodes .get (cfg .hotkey_pause ))#line:61
        O00O0O000O00OO0O0 =win32api .GetKeyState (Keyboard .KeyCodes .get (cfg .hotkey_reload_config ))#line:63
        if O00O0O000O00OO0O0 !=OO00O0OOOO0O00O0O :#line:64
            if O00O0O000O00OO0O0 ==1 or O00O0O000O00OO0O0 ==0 :#line:65
                cfg .Read (verbose =True )#line:66
                frames .reload_capture ()#line:67
                mouse_worker .Update_settings ()#line:68
        OO00O0OOOO0O00O0O =O00O0O000O00OO0O0 #line:69
        O0O00OO0OOO000OOO =frames .get_new_frame ()#line:71
        O00O0OO0OO00O00OO =OO00OOOOOO000OO00 .predict (source =O0O00OO0OOO000OOO ,stream =True ,cfg ='logic/game.yaml',imgsz =cfg .AI_image_size ,stream_buffer =False ,visualize =False ,augment =True ,agnostic_nms =False ,save =False ,conf =cfg .AI_conf ,iou =cfg .AI_iou ,device =cfg .AI_device ,half =False ,max_det =cfg .AI_max_det ,vid_stride =False ,classes =OO00OO000O0O000OO ,verbose =False ,show_boxes =False ,show_labels =False ,show_conf =False ,show =False )#line:93
        if cfg .show_window :#line:95
            OO0OO0OOO0OO0OOOO =int (cfg .detection_window_height *cfg .debug_window_scale_percent /100 )#line:96
            OOO00O000OOO000OO =int (cfg .detection_window_width *cfg .debug_window_scale_percent /100 )#line:97
            O0OO000O0O000OOO0 =(OOO00O000OOO000OO ,OO0OO0OOO0OO0OOOO )#line:98
            O0O00O0OOO0OOOOOO =O0O00OO0OOO000OOO #line:100
        for O00O0OO0000000O00 in O00O0OO0OO00O00OO :#line:102
            if cfg .show_window and cfg .show_speed ==True :#line:103
                O0O00O0OOO0OOOOOO =speed (O0O00O0OOO0OOOOOO ,O00O0OO0000000O00 .speed ['preprocess'],O00O0OO0000000O00 .speed ['inference'],O00O0OO0000000O00 .speed ['postprocess'])#line:104
            if len (O00O0OO0000000O00 .boxes ):#line:106
                if OOOO0O000O00OOO0O ==0 :#line:107
                    for OO0OO00OO00000000 in O00O0OO0000000O00 .boxes :#line:108
                        OOO0OO000O0OOOO00 =int (OO0OO00OO00000000 .cls .item ())#line:109
                        if not cfg .disable_headshot :#line:110
                            OOOO000000OO00O0O .append (Targets (*OO0OO00OO00000000 .xywh [0 ],OOO0OO000O0OOOO00 ))#line:111
                        elif OOO0OO000O0OOOO00 in (0 ,1 ,5 ,6 ):#line:112
                            OOOO000000OO00O0O .append (Targets (*OO0OO00OO00000000 .xywh [0 ],OOO0OO000O0OOOO00 ))#line:113
                    if not cfg .disable_headshot :#line:115
                        OOOO000000OO00O0O .sort (key =lambda OO000O0OOOO00OOOO :(OO000O0OOOO00OOOO .cls !=7 ,OO000O0OOOO00OOOO .distance ))#line:116
                    else :#line:117
                        OOOO000000OO00O0O .sort (key =lambda O00000OO0OOO00O00 :O00000OO0OOO00O00 .distance ,reverse =False )#line:118
                    try :#line:119
                        OOO0OO00O0OOOOOOO =OOOO000000OO00O0O [0 ]#line:120
                        mouse_worker .queue .put ((OOO0OO00O0OOOOOOO .mouse_x ,OOO0OO00O0OOOOOOO .mouse_y ,OOO0OO00O0OOOOOOO .x ,OOO0OO00O0OOOOOOO .y ,OOO0OO00O0OOOOOOO .w ,OOO0OO00O0OOOOOOO .h ,OOO0OO00O0OOOOOOO .distance ))#line:128
                        if cfg .show_window and cfg .show_target_line :#line:129
                            draw_target_line (annotated_frame =O0O00O0OOO0OOOOOO ,screen_x_center =cfg .detection_window_width /2 ,screen_y_center =cfg .detection_window_height /2 ,target_x =OOO0OO00O0OOOOOOO .mouse_x +frames .screen_x_center ,target_y =OOO0OO00O0OOOOOOO .mouse_y +frames .screen_y_center +cfg .body_y_offset /OOO0OO00O0OOOOOOO .h )#line:130
                    except IndexError :#line:131
                        mouse_worker .queue .put (None )#line:132
                        OOOO000000OO00O0O .clear ()#line:133
                    OOOO000000OO00O0O .clear ()#line:134
                else :pass #line:135
                if cfg .show_window and cfg .show_boxes :#line:137
                    draw_helpers (annotated_frame =O0O00O0OOO0OOOOOO ,boxes =O00O0OO0000000O00 .boxes )#line:138
            else :#line:139
                mouse_worker .queue .put (None )#line:140
        if cfg .show_window and cfg .show_fps :#line:142
            OO0OO0OOOOOOOO00O =time .time ()#line:143
            OOOOO0OOO00OO000O =1 /(OO0OO0OOOOOOOO00O -OO0OO00000OOOO00O )#line:144
            OO0OO00000OOOO00O =OO0OO0OOOOOOOO00O #line:145
            if cfg .show_speed :#line:147
                cv2 .putText (O0O00O0OOO0OOOOOO ,'FPS: {0}'.format (str (int (OOOOO0OOO00OO000O ))),(10 ,100 ),cv2 .FONT_HERSHEY_SIMPLEX ,0.6 ,(0 ,255 ,0 ),1 ,cv2 .LINE_AA )#line:148
            else :#line:149
                cv2 .putText (O0O00O0OOO0OOOOOO ,'FPS: {0}'.format (str (int (OOOOO0OOO00OO000O ))),(10 ,20 ),cv2 .FONT_HERSHEY_SIMPLEX ,0.6 ,(0 ,255 ,0 ),1 ,cv2 .LINE_AA )#line:150
        if win32api .GetAsyncKeyState (Keyboard .KeyCodes .get (cfg .hotkey_exit ))&0xFF :#line:152
            if cfg .show_window :#line:153
                cv2 .destroyWindow (cfg .debug_window_name )#line:154
            frames .Quit ()#line:155
            break #line:156
        if cfg .show_window :#line:158
            try :#line:159
                cv2 .resizeWindow (cfg .debug_window_name ,O0OO000O0O000OOO0 )#line:160
            except :exit (0 )#line:161
            OOOO000OOO000OO0O =cv2 .resize (O0O00O0OOO0OOOOOO ,O0OO000O0O000OOO0 ,cv2 .INTER_NEAREST )#line:162
            cv2 .imshow (cfg .debug_window_name ,OOOO000OOO000OO0O )#line:163
            if cv2 .waitKey (1 )&0xFF ==ord ('q'):#line:164
                break #line:165
if __name__ =="__main__":#line:167
    frames =Capture ()#line:168
    mouse_worker =MouseThread ()#line:169
    init ()