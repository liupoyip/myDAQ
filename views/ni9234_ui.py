# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ni9234.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QGroupBox, QLabel, QLayout,
    QLineEdit, QPushButton, QSizePolicy, QSlider,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_NI9234(object):
    def setupUi(self, NI9234):
        if not NI9234.objectName():
            NI9234.setObjectName(u"NI9234")
        NI9234.setEnabled(True)
        NI9234.resize(1600, 900)
        self.ControlButtons_GroupBox = QGroupBox(NI9234)
        self.ControlButtons_GroupBox.setObjectName(u"ControlButtons_GroupBox")
        self.ControlButtons_GroupBox.setGeometry(QRect(20, 780, 331, 80))
        self.Start_PushButton = QPushButton(self.ControlButtons_GroupBox)
        self.Start_PushButton.setObjectName(u"Start_PushButton")
        self.Start_PushButton.setGeometry(QRect(10, 50, 91, 24))
        self.Stop_PushButton = QPushButton(self.ControlButtons_GroupBox)
        self.Stop_PushButton.setObjectName(u"Stop_PushButton")
        self.Stop_PushButton.setGeometry(QRect(110, 50, 91, 24))
        self.Reset_PushButton = QPushButton(self.ControlButtons_GroupBox)
        self.Reset_PushButton.setObjectName(u"Reset_PushButton")
        self.Reset_PushButton.setGeometry(QRect(210, 50, 91, 24))
        self.CreateTask_PushButton = QPushButton(self.ControlButtons_GroupBox)
        self.CreateTask_PushButton.setObjectName(u"CreateTask_PushButton")
        self.CreateTask_PushButton.setGeometry(QRect(10, 20, 90, 24))
        self.ClearTask_PushButton = QPushButton(self.ControlButtons_GroupBox)
        self.ClearTask_PushButton.setObjectName(u"ClearTask_PushButton")
        self.ClearTask_PushButton.setGeometry(QRect(110, 20, 90, 24))
        self.WriteFile_GroupBox = QGroupBox(NI9234)
        self.WriteFile_GroupBox.setObjectName(u"WriteFile_GroupBox")
        self.WriteFile_GroupBox.setGeometry(QRect(20, 690, 341, 81))
        self.WriteFile_CheckBox = QCheckBox(self.WriteFile_GroupBox)
        self.WriteFile_CheckBox.setObjectName(u"WriteFile_CheckBox")
        self.WriteFile_CheckBox.setEnabled(False)
        self.WriteFile_CheckBox.setGeometry(QRect(140, 20, 71, 20))
        self.WriteFile_LineEdit = QLineEdit(self.WriteFile_GroupBox)
        self.WriteFile_LineEdit.setObjectName(u"WriteFile_LineEdit")
        self.WriteFile_LineEdit.setEnabled(False)
        self.WriteFile_LineEdit.setGeometry(QRect(100, 50, 201, 20))
        self.WriteFile_Label = QLabel(self.WriteFile_GroupBox)
        self.WriteFile_Label.setObjectName(u"WriteFile_Label")
        self.WriteFile_Label.setGeometry(QRect(10, 50, 101, 20))
        self.WriteFile_Label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.WriteFileType_ComboBox = QComboBox(self.WriteFile_GroupBox)
        self.WriteFileType_ComboBox.setObjectName(u"WriteFileType_ComboBox")
        self.WriteFileType_ComboBox.setEnabled(True)
        self.WriteFileType_ComboBox.setGeometry(QRect(10, 20, 111, 22))
        self.WriteFileType_ComboBox.setFrame(False)
        self.WriteFileStatus_Label = QLabel(self.WriteFile_GroupBox)
        self.WriteFileStatus_Label.setObjectName(u"WriteFileStatus_Label")
        self.WriteFileStatus_Label.setGeometry(QRect(220, 20, 91, 16))
        self.NowTime_Label = QLabel(NI9234)
        self.NowTime_Label.setObjectName(u"NowTime_Label")
        self.NowTime_Label.setGeometry(QRect(10, 880, 201, 16))
        self.PreparationSetting_Frame = QFrame(NI9234)
        self.PreparationSetting_Frame.setObjectName(u"PreparationSetting_Frame")
        self.PreparationSetting_Frame.setGeometry(QRect(10, 150, 361, 331))
        self.PreparationSetting_Frame.setFrameShape(QFrame.StyledPanel)
        self.PreparationSetting_Frame.setFrameShadow(QFrame.Raised)
        self.DAQParameters_GroupBox = QGroupBox(self.PreparationSetting_Frame)
        self.DAQParameters_GroupBox.setObjectName(u"DAQParameters_GroupBox")
        self.DAQParameters_GroupBox.setGeometry(QRect(10, 60, 340, 101))
        self.layoutWidget = QWidget(self.DAQParameters_GroupBox)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 20, 321, 71))
        self.DAQParameters_VerticalLayout = QVBoxLayout(self.layoutWidget)
        self.DAQParameters_VerticalLayout.setObjectName(u"DAQParameters_VerticalLayout")
        self.DAQParameters_VerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.SampleRate_Frame = QFrame(self.layoutWidget)
        self.SampleRate_Frame.setObjectName(u"SampleRate_Frame")
        self.SampleRate_Frame.setEnabled(True)
        self.SampleRate_Frame.setFrameShape(QFrame.NoFrame)
        self.SampleRate_Frame.setFrameShadow(QFrame.Plain)
        self.SampleRate_HorizontalSlider = QSlider(self.SampleRate_Frame)
        self.SampleRate_HorizontalSlider.setObjectName(u"SampleRate_HorizontalSlider")
        self.SampleRate_HorizontalSlider.setGeometry(QRect(160, 5, 80, 20))
        self.SampleRate_HorizontalSlider.setMinimum(0)
        self.SampleRate_HorizontalSlider.setMaximum(99)
        self.SampleRate_HorizontalSlider.setValue(0)
        self.SampleRate_HorizontalSlider.setSliderPosition(0)
        self.SampleRate_HorizontalSlider.setOrientation(Qt.Horizontal)
        self.SampleRate_SpinBox = QSpinBox(self.SampleRate_Frame)
        self.SampleRate_SpinBox.setObjectName(u"SampleRate_SpinBox")
        self.SampleRate_SpinBox.setGeometry(QRect(250, 5, 60, 20))
        self.SampleRate_SpinBox.setFrame(False)
        self.SampleRate_SpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.SampleRate_SpinBox.setSpecialValueText(u"")
        self.SampleRate_SpinBox.setMinimum(0)
        self.SampleRate_SpinBox.setMaximum(99)
        self.SampleRate_SpinBox.setValue(0)
        self.SampleRate_Label = QLabel(self.SampleRate_Frame)
        self.SampleRate_Label.setObjectName(u"SampleRate_Label")
        self.SampleRate_Label.setGeometry(QRect(10, 5, 140, 20))
        self.SampleRate_Label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.SampleRate_Label.setIndent(-1)

        self.DAQParameters_VerticalLayout.addWidget(self.SampleRate_Frame)

        self.FrameDuration_Frame = QFrame(self.layoutWidget)
        self.FrameDuration_Frame.setObjectName(u"FrameDuration_Frame")
        self.FrameDuration_Frame.setEnabled(True)
        self.FrameDuration_Frame.setFrameShape(QFrame.NoFrame)
        self.FrameDuration_Frame.setFrameShadow(QFrame.Plain)
        self.FrameDuration_HorizontalSlider = QSlider(self.FrameDuration_Frame)
        self.FrameDuration_HorizontalSlider.setObjectName(u"FrameDuration_HorizontalSlider")
        self.FrameDuration_HorizontalSlider.setGeometry(QRect(160, 5, 80, 20))
        self.FrameDuration_HorizontalSlider.setMinimum(0)
        self.FrameDuration_HorizontalSlider.setMaximum(99)
        self.FrameDuration_HorizontalSlider.setValue(0)
        self.FrameDuration_HorizontalSlider.setSliderPosition(0)
        self.FrameDuration_HorizontalSlider.setOrientation(Qt.Horizontal)
        self.FrameDuration_SpinBox = QSpinBox(self.FrameDuration_Frame)
        self.FrameDuration_SpinBox.setObjectName(u"FrameDuration_SpinBox")
        self.FrameDuration_SpinBox.setGeometry(QRect(250, 5, 60, 20))
        self.FrameDuration_SpinBox.setFrame(False)
        self.FrameDuration_SpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.FrameDuration_SpinBox.setSpecialValueText(u"")
        self.FrameDuration_SpinBox.setMinimum(0)
        self.FrameDuration_SpinBox.setMaximum(99)
        self.FrameDuration_SpinBox.setValue(0)
        self.FrameDuration_Label = QLabel(self.FrameDuration_Frame)
        self.FrameDuration_Label.setObjectName(u"FrameDuration_Label")
        self.FrameDuration_Label.setGeometry(QRect(10, 5, 140, 20))
        self.FrameDuration_Label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.FrameDuration_Label.setIndent(-1)

        self.DAQParameters_VerticalLayout.addWidget(self.FrameDuration_Frame)

        self.ChannelOption_GroupBox = QGroupBox(self.PreparationSetting_Frame)
        self.ChannelOption_GroupBox.setObjectName(u"ChannelOption_GroupBox")
        self.ChannelOption_GroupBox.setGeometry(QRect(10, 160, 341, 161))
        self.layoutWidget1 = QWidget(self.ChannelOption_GroupBox)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 20, 321, 131))
        self.ChannelOption_VerticalLayout = QVBoxLayout(self.layoutWidget1)
        self.ChannelOption_VerticalLayout.setSpacing(0)
        self.ChannelOption_VerticalLayout.setObjectName(u"ChannelOption_VerticalLayout")
        self.ChannelOption_VerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.Channel0_Frame = QFrame(self.layoutWidget1)
        self.Channel0_Frame.setObjectName(u"Channel0_Frame")
        self.Channel0_Frame.setFrameShape(QFrame.NoFrame)
        self.Channel0_Frame.setFrameShadow(QFrame.Plain)
        self.Channel0_CheckBox = QCheckBox(self.Channel0_Frame)
        self.Channel0_CheckBox.setObjectName(u"Channel0_CheckBox")
        self.Channel0_CheckBox.setGeometry(QRect(5, 5, 90, 22))
        self.Channel0_ComboBox = QComboBox(self.Channel0_Frame)
        self.Channel0_ComboBox.setObjectName(u"Channel0_ComboBox")
        self.Channel0_ComboBox.setGeometry(QRect(90, 5, 110, 22))
        self.Channel0_ComboBox.setFrame(False)

        self.ChannelOption_VerticalLayout.addWidget(self.Channel0_Frame)

        self.Channel1_Frame = QFrame(self.layoutWidget1)
        self.Channel1_Frame.setObjectName(u"Channel1_Frame")
        self.Channel1_Frame.setFrameShape(QFrame.NoFrame)
        self.Channel1_Frame.setFrameShadow(QFrame.Plain)
        self.Channel1_CheckBox = QCheckBox(self.Channel1_Frame)
        self.Channel1_CheckBox.setObjectName(u"Channel1_CheckBox")
        self.Channel1_CheckBox.setGeometry(QRect(5, 5, 90, 22))
        self.Channel1_ComboBox = QComboBox(self.Channel1_Frame)
        self.Channel1_ComboBox.setObjectName(u"Channel1_ComboBox")
        self.Channel1_ComboBox.setGeometry(QRect(90, 5, 110, 22))
        self.Channel1_ComboBox.setFrame(False)

        self.ChannelOption_VerticalLayout.addWidget(self.Channel1_Frame)

        self.Channel2_Frame = QFrame(self.layoutWidget1)
        self.Channel2_Frame.setObjectName(u"Channel2_Frame")
        self.Channel2_Frame.setFrameShape(QFrame.NoFrame)
        self.Channel2_Frame.setFrameShadow(QFrame.Plain)
        self.Channel2_CheckBox = QCheckBox(self.Channel2_Frame)
        self.Channel2_CheckBox.setObjectName(u"Channel2_CheckBox")
        self.Channel2_CheckBox.setGeometry(QRect(5, 5, 90, 22))
        self.Channel2_ComboBox = QComboBox(self.Channel2_Frame)
        self.Channel2_ComboBox.setObjectName(u"Channel2_ComboBox")
        self.Channel2_ComboBox.setGeometry(QRect(90, 5, 110, 22))
        self.Channel2_ComboBox.setFrame(False)

        self.ChannelOption_VerticalLayout.addWidget(self.Channel2_Frame)

        self.Channel3_Frame = QFrame(self.layoutWidget1)
        self.Channel3_Frame.setObjectName(u"Channel3_Frame")
        self.Channel3_Frame.setFrameShape(QFrame.NoFrame)
        self.Channel3_Frame.setFrameShadow(QFrame.Plain)
        self.Channel3_CheckBox = QCheckBox(self.Channel3_Frame)
        self.Channel3_CheckBox.setObjectName(u"Channel3_CheckBox")
        self.Channel3_CheckBox.setGeometry(QRect(5, 5, 90, 22))
        self.Channel3_ComboBox = QComboBox(self.Channel3_Frame)
        self.Channel3_ComboBox.setObjectName(u"Channel3_ComboBox")
        self.Channel3_ComboBox.setGeometry(QRect(90, 5, 110, 22))
        self.Channel3_ComboBox.setFrame(False)

        self.ChannelOption_VerticalLayout.addWidget(self.Channel3_Frame)

        self.Task_GroupBox = QGroupBox(self.PreparationSetting_Frame)
        self.Task_GroupBox.setObjectName(u"Task_GroupBox")
        self.Task_GroupBox.setGeometry(QRect(10, 0, 341, 51))
        self.TaskName_Label = QLabel(self.Task_GroupBox)
        self.TaskName_Label.setObjectName(u"TaskName_Label")
        self.TaskName_Label.setGeometry(QRect(10, 20, 60, 22))
        self.TaskName_Label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.TaskName_LineEdit = QLineEdit(self.Task_GroupBox)
        self.TaskName_LineEdit.setObjectName(u"TaskName_LineEdit")
        self.TaskName_LineEdit.setGeometry(QRect(90, 20, 241, 22))
        self.TaskName_LineEdit.setFrame(False)
        self.gridLayoutWidget = QWidget(NI9234)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(380, 10, 1211, 881))
        self.Charts_GridLayout = QGridLayout(self.gridLayoutWidget)
        self.Charts_GridLayout.setSpacing(0)
        self.Charts_GridLayout.setObjectName(u"Charts_GridLayout")
        self.Charts_GridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.Charts_GridLayout.setContentsMargins(0, 0, 0, 0)
        self.FunctionTest_Pushbutton = QPushButton(NI9234)
        self.FunctionTest_Pushbutton.setObjectName(u"FunctionTest_Pushbutton")
        self.FunctionTest_Pushbutton.setGeometry(QRect(280, 870, 75, 24))
        self.Visualize_Groupbox = QGroupBox(NI9234)
        self.Visualize_Groupbox.setObjectName(u"Visualize_Groupbox")
        self.Visualize_Groupbox.setGeometry(QRect(10, 480, 361, 211))
        self.VisualizeSwitch_Checkbox = QCheckBox(self.Visualize_Groupbox)
        self.VisualizeSwitch_Checkbox.setObjectName(u"VisualizeSwitch_Checkbox")
        self.VisualizeSwitch_Checkbox.setGeometry(QRect(20, 20, 71, 20))
        self.ChartParameters_GroupBox = QGroupBox(self.Visualize_Groupbox)
        self.ChartParameters_GroupBox.setObjectName(u"ChartParameters_GroupBox")
        self.ChartParameters_GroupBox.setGeometry(QRect(10, 40, 341, 161))
        self.layoutWidget2 = QWidget(self.ChartParameters_GroupBox)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 20, 321, 131))
        self.ChartParameters_VerticalLayout = QVBoxLayout(self.layoutWidget2)
        self.ChartParameters_VerticalLayout.setSpacing(0)
        self.ChartParameters_VerticalLayout.setObjectName(u"ChartParameters_VerticalLayout")
        self.ChartParameters_VerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.BufferRate_Frame = QFrame(self.layoutWidget2)
        self.BufferRate_Frame.setObjectName(u"BufferRate_Frame")
        self.BufferRate_Frame.setEnabled(True)
        self.BufferRate_Frame.setFrameShape(QFrame.NoFrame)
        self.BufferRate_Frame.setFrameShadow(QFrame.Plain)
        self.BufferRate_HorizontalSlider = QSlider(self.BufferRate_Frame)
        self.BufferRate_HorizontalSlider.setObjectName(u"BufferRate_HorizontalSlider")
        self.BufferRate_HorizontalSlider.setGeometry(QRect(160, 5, 80, 20))
        self.BufferRate_HorizontalSlider.setMinimum(0)
        self.BufferRate_HorizontalSlider.setMaximum(99)
        self.BufferRate_HorizontalSlider.setValue(0)
        self.BufferRate_HorizontalSlider.setSliderPosition(0)
        self.BufferRate_HorizontalSlider.setOrientation(Qt.Horizontal)
        self.BufferRate_SpinBox = QSpinBox(self.BufferRate_Frame)
        self.BufferRate_SpinBox.setObjectName(u"BufferRate_SpinBox")
        self.BufferRate_SpinBox.setGeometry(QRect(250, 5, 60, 20))
        self.BufferRate_SpinBox.setFrame(False)
        self.BufferRate_SpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.BufferRate_SpinBox.setSpecialValueText(u"")
        self.BufferRate_SpinBox.setMinimum(0)
        self.BufferRate_SpinBox.setMaximum(99)
        self.BufferRate_SpinBox.setValue(0)
        self.BufferRate_Label = QLabel(self.BufferRate_Frame)
        self.BufferRate_Label.setObjectName(u"BufferRate_Label")
        self.BufferRate_Label.setGeometry(QRect(10, 5, 140, 20))
        self.BufferRate_Label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.BufferRate_Label.setIndent(-1)

        self.ChartParameters_VerticalLayout.addWidget(self.BufferRate_Frame)

        self.ChartUpdateInterval_Frame = QFrame(self.layoutWidget2)
        self.ChartUpdateInterval_Frame.setObjectName(u"ChartUpdateInterval_Frame")
        self.ChartUpdateInterval_Frame.setEnabled(True)
        self.ChartUpdateInterval_Frame.setFrameShape(QFrame.NoFrame)
        self.ChartUpdateInterval_Frame.setFrameShadow(QFrame.Plain)
        self.ChartUpdateInterval_HorizontalSlider = QSlider(self.ChartUpdateInterval_Frame)
        self.ChartUpdateInterval_HorizontalSlider.setObjectName(u"ChartUpdateInterval_HorizontalSlider")
        self.ChartUpdateInterval_HorizontalSlider.setGeometry(QRect(160, 5, 80, 20))
        self.ChartUpdateInterval_HorizontalSlider.setMinimum(0)
        self.ChartUpdateInterval_HorizontalSlider.setMaximum(100)
        self.ChartUpdateInterval_HorizontalSlider.setSingleStep(1)
        self.ChartUpdateInterval_HorizontalSlider.setPageStep(1)
        self.ChartUpdateInterval_HorizontalSlider.setValue(0)
        self.ChartUpdateInterval_HorizontalSlider.setSliderPosition(0)
        self.ChartUpdateInterval_HorizontalSlider.setOrientation(Qt.Horizontal)
        self.ChartUpdateInterval_SpinBox = QSpinBox(self.ChartUpdateInterval_Frame)
        self.ChartUpdateInterval_SpinBox.setObjectName(u"ChartUpdateInterval_SpinBox")
        self.ChartUpdateInterval_SpinBox.setGeometry(QRect(250, 5, 60, 20))
        self.ChartUpdateInterval_SpinBox.setFrame(False)
        self.ChartUpdateInterval_SpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.ChartUpdateInterval_SpinBox.setSpecialValueText(u"")
        self.ChartUpdateInterval_SpinBox.setMinimum(0)
        self.ChartUpdateInterval_SpinBox.setMaximum(100)
        self.ChartUpdateInterval_Label = QLabel(self.ChartUpdateInterval_Frame)
        self.ChartUpdateInterval_Label.setObjectName(u"ChartUpdateInterval_Label")
        self.ChartUpdateInterval_Label.setGeometry(QRect(10, 5, 140, 20))
        self.ChartUpdateInterval_Label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.ChartUpdateInterval_Label.setIndent(-1)

        self.ChartParameters_VerticalLayout.addWidget(self.ChartUpdateInterval_Frame)

        self.WaveDownSample_Frame = QFrame(self.layoutWidget2)
        self.WaveDownSample_Frame.setObjectName(u"WaveDownSample_Frame")
        self.WaveDownSample_Frame.setEnabled(True)
        self.WaveDownSample_Frame.setFrameShape(QFrame.NoFrame)
        self.WaveDownSample_Frame.setFrameShadow(QFrame.Plain)
        self.WaveDownSample_HorizontalSlider = QSlider(self.WaveDownSample_Frame)
        self.WaveDownSample_HorizontalSlider.setObjectName(u"WaveDownSample_HorizontalSlider")
        self.WaveDownSample_HorizontalSlider.setGeometry(QRect(160, 5, 80, 20))
        self.WaveDownSample_HorizontalSlider.setMinimum(0)
        self.WaveDownSample_HorizontalSlider.setMaximum(5)
        self.WaveDownSample_HorizontalSlider.setValue(0)
        self.WaveDownSample_HorizontalSlider.setSliderPosition(0)
        self.WaveDownSample_HorizontalSlider.setOrientation(Qt.Horizontal)
        self.WaveDownSample_SpinBox = QSpinBox(self.WaveDownSample_Frame)
        self.WaveDownSample_SpinBox.setObjectName(u"WaveDownSample_SpinBox")
        self.WaveDownSample_SpinBox.setGeometry(QRect(250, 5, 60, 20))
        self.WaveDownSample_SpinBox.setFrame(False)
        self.WaveDownSample_SpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.WaveDownSample_SpinBox.setSpecialValueText(u"")
        self.WaveDownSample_SpinBox.setMinimum(0)
        self.WaveDownSample_SpinBox.setMaximum(100)
        self.WaveDownSample_Label = QLabel(self.WaveDownSample_Frame)
        self.WaveDownSample_Label.setObjectName(u"WaveDownSample_Label")
        self.WaveDownSample_Label.setGeometry(QRect(10, 5, 140, 20))
        self.WaveDownSample_Label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.WaveDownSample_Label.setIndent(-1)

        self.ChartParameters_VerticalLayout.addWidget(self.WaveDownSample_Frame)

        self.SpectrumDownSample_Frame = QFrame(self.layoutWidget2)
        self.SpectrumDownSample_Frame.setObjectName(u"SpectrumDownSample_Frame")
        self.SpectrumDownSample_Frame.setEnabled(True)
        self.SpectrumDownSample_Frame.setFrameShape(QFrame.NoFrame)
        self.SpectrumDownSample_Frame.setFrameShadow(QFrame.Plain)
        self.SpectrumDownSample_HorizontalSlider = QSlider(self.SpectrumDownSample_Frame)
        self.SpectrumDownSample_HorizontalSlider.setObjectName(u"SpectrumDownSample_HorizontalSlider")
        self.SpectrumDownSample_HorizontalSlider.setGeometry(QRect(160, 5, 80, 20))
        self.SpectrumDownSample_HorizontalSlider.setMinimum(0)
        self.SpectrumDownSample_HorizontalSlider.setMaximum(5)
        self.SpectrumDownSample_HorizontalSlider.setValue(0)
        self.SpectrumDownSample_HorizontalSlider.setSliderPosition(0)
        self.SpectrumDownSample_HorizontalSlider.setOrientation(Qt.Horizontal)
        self.SpectrumDownSample_SpinBox = QSpinBox(self.SpectrumDownSample_Frame)
        self.SpectrumDownSample_SpinBox.setObjectName(u"SpectrumDownSample_SpinBox")
        self.SpectrumDownSample_SpinBox.setGeometry(QRect(250, 5, 60, 20))
        self.SpectrumDownSample_SpinBox.setFrame(False)
        self.SpectrumDownSample_SpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.SpectrumDownSample_SpinBox.setSpecialValueText(u"")
        self.SpectrumDownSample_SpinBox.setMinimum(0)
        self.SpectrumDownSample_SpinBox.setMaximum(100)
        self.SpectrumDownSample_Label = QLabel(self.SpectrumDownSample_Frame)
        self.SpectrumDownSample_Label.setObjectName(u"SpectrumDownSample_Label")
        self.SpectrumDownSample_Label.setGeometry(QRect(10, 5, 140, 20))
        self.SpectrumDownSample_Label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.SpectrumDownSample_Label.setIndent(-1)

        self.ChartParameters_VerticalLayout.addWidget(self.SpectrumDownSample_Frame)

        self.MachineInfo_GroupBox = QGroupBox(NI9234)
        self.MachineInfo_GroupBox.setObjectName(u"MachineInfo_GroupBox")
        self.MachineInfo_GroupBox.setGeometry(QRect(20, 90, 341, 51))
        self.MachineID_Label = QLabel(self.MachineInfo_GroupBox)
        self.MachineID_Label.setObjectName(u"MachineID_Label")
        self.MachineID_Label.setGeometry(QRect(10, 20, 61, 16))
        self.MachineID_LineEdit = QLineEdit(self.MachineInfo_GroupBox)
        self.MachineID_LineEdit.setObjectName(u"MachineID_LineEdit")
        self.MachineID_LineEdit.setGeometry(QRect(90, 20, 241, 22))
        self.ImportConfig_Pushbutton = QPushButton(NI9234)
        self.ImportConfig_Pushbutton.setObjectName(u"ImportConfig_Pushbutton")
        self.ImportConfig_Pushbutton.setGeometry(QRect(300, 40, 51, 24))
        self.ImportConfig_Label = QLabel(NI9234)
        self.ImportConfig_Label.setObjectName(u"ImportConfig_Label")
        self.ImportConfig_Label.setGeometry(QRect(30, 40, 31, 16))
        self.ImportConfigPath_LineEdit = QLineEdit(NI9234)
        self.ImportConfigPath_LineEdit.setObjectName(u"ImportConfigPath_LineEdit")
        self.ImportConfigPath_LineEdit.setEnabled(False)
        self.ImportConfigPath_LineEdit.setGeometry(QRect(70, 40, 221, 22))

        self.retranslateUi(NI9234)
        self.SampleRate_HorizontalSlider.valueChanged.connect(self.SampleRate_SpinBox.setValue)
        self.SampleRate_SpinBox.valueChanged.connect(self.SampleRate_HorizontalSlider.setValue)
        self.FrameDuration_HorizontalSlider.valueChanged.connect(self.FrameDuration_SpinBox.setValue)
        self.FrameDuration_SpinBox.valueChanged.connect(self.FrameDuration_HorizontalSlider.setValue)
        self.ChartUpdateInterval_HorizontalSlider.valueChanged.connect(self.ChartUpdateInterval_SpinBox.setValue)
        self.ChartUpdateInterval_SpinBox.valueChanged.connect(self.ChartUpdateInterval_HorizontalSlider.setValue)
        self.WaveDownSample_HorizontalSlider.valueChanged.connect(self.WaveDownSample_SpinBox.setValue)
        self.WaveDownSample_SpinBox.valueChanged.connect(self.WaveDownSample_HorizontalSlider.setValue)
        self.BufferRate_HorizontalSlider.valueChanged.connect(self.BufferRate_SpinBox.setValue)
        self.BufferRate_SpinBox.valueChanged.connect(self.BufferRate_HorizontalSlider.setValue)

        QMetaObject.connectSlotsByName(NI9234)
    # setupUi

    def retranslateUi(self, NI9234):
        NI9234.setWindowTitle(QCoreApplication.translate("NI9234", u"NI9234", None))
        self.ControlButtons_GroupBox.setTitle(QCoreApplication.translate("NI9234", u"Control", None))
        self.Start_PushButton.setText(QCoreApplication.translate("NI9234", u"Start", None))
        self.Stop_PushButton.setText(QCoreApplication.translate("NI9234", u"Stop", None))
        self.Reset_PushButton.setText(QCoreApplication.translate("NI9234", u"Reset", None))
        self.CreateTask_PushButton.setText(QCoreApplication.translate("NI9234", u"Create Task", None))
        self.ClearTask_PushButton.setText(QCoreApplication.translate("NI9234", u"Clear Task", None))
        self.WriteFile_GroupBox.setTitle(QCoreApplication.translate("NI9234", u"Write File", None))
        self.WriteFile_CheckBox.setText(QCoreApplication.translate("NI9234", u"On/Off", None))
        self.WriteFile_Label.setText(QCoreApplication.translate("NI9234", u"Data Directory", None))
        self.WriteFileStatus_Label.setText(QCoreApplication.translate("NI9234", u"Status:", None))
        self.NowTime_Label.setText(QCoreApplication.translate("NI9234", u"Now Time", None))
        self.DAQParameters_GroupBox.setTitle(QCoreApplication.translate("NI9234", u"DAQ Parameters", None))
        self.SampleRate_Label.setText(QCoreApplication.translate("NI9234", u"Sampling Rate (Hz)", None))
        self.FrameDuration_Label.setText(QCoreApplication.translate("NI9234", u"Frame Duration (ms)", None))
        self.ChannelOption_GroupBox.setTitle(QCoreApplication.translate("NI9234", u"Channel Option", None))
        self.Channel0_CheckBox.setText(QCoreApplication.translate("NI9234", u"Channel 0", None))
        self.Channel1_CheckBox.setText(QCoreApplication.translate("NI9234", u"Channel 1", None))
        self.Channel2_CheckBox.setText(QCoreApplication.translate("NI9234", u"Channel 2", None))
        self.Channel3_CheckBox.setText(QCoreApplication.translate("NI9234", u"Channel 3", None))
        self.Task_GroupBox.setTitle(QCoreApplication.translate("NI9234", u"Task", None))
        self.TaskName_Label.setText(QCoreApplication.translate("NI9234", u"Task Name", None))
        self.TaskName_LineEdit.setInputMask("")
        self.TaskName_LineEdit.setText("")
        self.FunctionTest_Pushbutton.setText(QCoreApplication.translate("NI9234", u"Func Test", None))
        self.Visualize_Groupbox.setTitle(QCoreApplication.translate("NI9234", u"Visualize", None))
        self.VisualizeSwitch_Checkbox.setText(QCoreApplication.translate("NI9234", u"On/Off", None))
        self.ChartParameters_GroupBox.setTitle(QCoreApplication.translate("NI9234", u"Chart Parameters", None))
        self.BufferRate_Label.setText(QCoreApplication.translate("NI9234", u"Buffer Rate", None))
        self.ChartUpdateInterval_Label.setText(QCoreApplication.translate("NI9234", u"Update Interval (ms)", None))
        self.WaveDownSample_Label.setText(QCoreApplication.translate("NI9234", u"Wave Down Sample", None))
        self.SpectrumDownSample_Label.setText(QCoreApplication.translate("NI9234", u"Spectrum Down Sample", None))
        self.MachineInfo_GroupBox.setTitle(QCoreApplication.translate("NI9234", u"Machine Info", None))
        self.MachineID_Label.setText(QCoreApplication.translate("NI9234", u"Machine ID", None))
        self.MachineID_LineEdit.setText("")
        self.ImportConfig_Pushbutton.setText(QCoreApplication.translate("NI9234", u"Import", None))
        self.ImportConfig_Label.setText(QCoreApplication.translate("NI9234", u"path:", None))
    # retranslateUi

