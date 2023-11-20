**目標**:
盡速把UI和量測功能做出來，能放在高明現場量測數據

# 連續型資料所需之資料備註
```
properties format: 
{
    machine_ID,
    [sensor_model_0, sensor_model_1, ...],
    [data_name_0, data_name_1, ...],
    [physical_unit_0, physical_unit_1, ],
    DAQ_model,
    start_time,
    sampling_rate,
    end_time,
    chunk_length,
    chunk_count,
    
}
```

- 以下資料對應各資料的index
  - `sensor_model` : sensor型號
  - `data_name` : sensor所量測的數據名稱定義
  - `physical_unit` : 對應的sensor物理單位

### reference
https://stackoverflow.com/questions/26698628/mvc-design-with-qt-designer-and-pyqt-pyside