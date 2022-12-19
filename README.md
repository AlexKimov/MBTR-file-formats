## About
File formats and tools for Mercedes Benz Truck Racing (2000).

## Formats
| № | Format/Ext  | Template (010 Editor) |  Kaitai struct | Description   |
| :-- | :------- | :-- |  :-- | :-- |
|  **1**  | SYN |  [SYN.bt](https://github.com/AlexKimov/MBTR-file-formats/blob/master/templates/010editor/SYN.bt) |  | resource archives (compressed) |
|  **2**  | OIF |  [OIF.bt](https://github.com/AlexKimov/MBTR-file-formats/blob/master/templates/010editor/OIF.bt) |  | 3d models |

    1. Get 010Editor.
    2. Open file you need and apply template file (Templates - Open template).

## Tools

#### QuickBMS 

| № | .bat file | Script  | Description   |
| :-- | :------- | :-------  | :-- |
|  **1**  | [run.bat](https://github.com/AlexKimov/MBTR-file-formats/blob/master/scripts/bms/run.bat) | [mbtr.bms](https://github.com/AlexKimov/MBTR-file-formats/blob/master/scripts/bms/mbtr.bms)  | unpack *.syn archives |

    1. Unpack latest quickbms version https://aluigi.altervista.org/quickbms.htm to folder.
    2. Open bat file and set path to game folder.
    3. Run bat file and check for unpacked files.
    
#### Noesis

| № | Plugin | Description   |
| :-- | :------- | :-------  | 
|  **1**  | [fmt_mbtr_syn.py](https://github.com/AlexKimov/MBTR-file-formats/blob/master/plugins/noesis/fmt_mbtr_syn.py)  | unpack *.syn archives |

    1. Get latest Noesis version.
    2. Put file to PathToNoesis/plugins/python.
    3. Open Noesis. 
    4, Open .syn archive.
        
----

Форматы файлов и инструменты для работы с файлами игр Mercedes Benz Truck Racing (2000).

## Форматы
| № | Формат | Template (010 Editor) | Описание   |
| :-- | :------- | :-- |  :-- | 
|  **1**  | SYN |  [SYN.bt](https://github.com/AlexKimov/MBTR-file-formats/blob/master/templates/010editor/SYN.bt) |  сжатый архив игры |
|  **2**  | OIF |  [OIF.bt](https://github.com/AlexKimov/MBTR-file-formats/blob/master/templates/010editor/OIF.bt) |  3d модели |
