#About 
Данный скрипт - это часть  математического и программного обеспечения экспертной геоинформационной системы для районирования территории по степени риска развития опасных экзогенных процессов.
Предназначен для визуализации результатов вычисления характеристик местности. Переносит данные о цвете из геопривязанного растра .tiff (geotiff) в геопривязанную 3D модель в формате .ply

#Libraries
Для работы скрипта необходимо установить библиотеки: 
os - для работы с файловой системой windows
time - для вычисления времени выполнения подзадач
plyfile - для работы с ply файлами (3D модель, облако точек)
gdal - для рабооты с геопривязанным растром .tiff
numpy, numba - для сокращения времени выполнения задач

#Install
conda install gdal
OR download file at https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal and
pip install (path_to_file)

conda install -c conda-forge plyfile 
OR pip install plyfile
conda install numba

#Run
перейти в папку RUN и запустить replaceColor.exe
ИЛИ
Для запуска скрипта необходимо запустить файл "main.py"

По желанию можно изменить имя экспортируемого файла:
"out_ply_file_name"

#Screnshot

![image](https://user-images.githubusercontent.com/58412734/112442173-89163480-8d86-11eb-8f7c-de2390174ef3.png)
