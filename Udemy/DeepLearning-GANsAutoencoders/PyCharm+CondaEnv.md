Para os imports funcionarem corretamente com o Anaconda, é necessário seguir os
seguintes passos:

(1) Descobrir o caminho do binário do Pycharm. No meu caso:
```
C:\Program Files\JetBrains\PyCharm Community Edition 2021.2.3\bin\pycharm64.exe
```

(2) Ativar o Conda Env através do Anaconda Console. No meu caso, os comandos foram:
```
conda env list
conda activate tf2_py39
```

(3) Rodar o Pycharm através do Anaconda console:
```
"C:\Program Files\JetBrains\PyCharm Community Edition 2021.2.3\bin\"pycharm64.exe
"C:\Program Files\JetBrains\PyCharm Community Edition 2021.2\bin\"pycharm64.exe
```
A partir daqui, bastou eu abrir o meu projeto, e as dependências foram carregadas 
corretametne. 

