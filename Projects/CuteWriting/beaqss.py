# 右下角按钮
qssbut = ("QPushButton{"
               "font-size:26px;"
               "color:#f2f2f2;"
               "font-family: 微软雅黑,宋体,Arial,Helvetica,Verdana,sans-serif; "
               "background-color: none;"
               "border:2px solid white;border-radius:10px;"
               "}"
               " "
               "QPushButton:hover{ "
               "font-size:26px;  "
               "color:#f2f2f2;  "
               "font-family: 微软雅黑,宋体,Arial,Helvetica,Verdana,sans-serif;  "
               "background-color: rgba(0,33,99, 150);"
               "border:2px solid white;border-radius:10px;"
               "}"
               " "
               "QPushButton:pressed{"
               "font-size:26px; "
               "color:#f2f2f2; "
               "font-family: 微软雅黑,宋体,Arial,Helvetica,Verdana,sans-serif;"
               "background-color: rgba(0,33,99, 255);"
               "border:2px solid white;border-radius:10px;"
               "padding-left:3px;"
               "padding-top:3px;"
               "} "
               )

# menu
menuqss = """
    QMenu {
        color:darkblue;
        background-color: skyblue; 
        border-radius:12px;
        padding:5px;
        font-size : 14px;
        font-weight : 900;
        margin:6px;
    }
    QMenu::item:text { 
        padding-left:10px;
        padding-right:10px;
    }
    QMenu::item:selected{ 
        color:#1aa3ff;
        background-color: #e5f5ff;
        border-radius:3px;
    }
    QMenu::separator{
        height:1px;
        background:#bbbbbb;
        margin:5px;
        margin-left:10px;
        margin-right:10px;
    }
"""

# toolqss
toolqss = """
    QToolButton
    {
        border:none;
        color: darkblue;
        background-color:rgba(120,127,131,0);
        width:95px;
        height:25px;
        font-weight : 400;
        font-family : 隶书;
    }
    QToolButton:!enabled{
        color: rgb(80,80,80);
    }
    
    QToolButton:checked
    {
        border:1px solid #607D8B;
        color:rgb(73,169,238);
        background-color:#546E7A;
    }
    
    QToolButton:hover
    {
        color:white;
        border:1px solid #78909C;
        background-color:#757575;
    }
    
    QToolButton:pressed
    {
        border:1px solid #607D8B;
        color:rgb(73,169,238);
        background-color:#546E7A;
    }
    QToolButton::menu-button
    {
        background-color:transparent;
    }
"""

# textedit
ttqss = """
    QScrollBar{
        border: 1px solid #999999;
        background:white;
        width:10px;
        height:10px;
        margin: 0px 0px 0px 0px;
        }
    QScrollBar::handle{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130), stop:1 rgb(32, 47, 130));
        min-height: 0px;
    }
    QScrollBar::add-line{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130), stop:1 rgb(32, 47, 130));
        height: 0px;
        bcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130), stop:1 rgb(32, 47, 130));
        height: 0 px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }
"""

# sliderqss
sliderqss = """
    QSlider::groove:horizontal{ 
            height: 60px; 
            left: 0px; 
            right: 0px; 
            border:0px;   
            border-radius:6px;    
            background-color : darkblue;
     } 
     QSlider::handle:horizontal{ 
            width:  15px; 
            height: 50px; 
            margin-top: -20px; 
            margin-left: 0px; 
            margin-bottom: -20px; 
            margin-right: 0px; 
            border-image:url(src/picture/formu.png);
    } 
    QSlider::sub-page:horizontal{
           background:rgba(80,166,234,1);         
    }
"""

# laqss
laqss = """
    QLabel {
        border-bottom-left-radius: 10px;
        border-top-left-radius: 10px;
        background-color : gold;
        font-size : 18px;
        color : darkblue;
        font-family : 微软雅黑;
        font-weight : 700;
    }
"""