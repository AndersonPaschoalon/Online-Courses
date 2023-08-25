from matplotlib import pyplot as plt
from matplotlib import style
import mysignals as sig
import os


OUT_DIR = "10"

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)


style.use('ggplot')
# queremos fazer um plot com 3 subplots
f, plt_array = plt.subplots(3, sharex=True)
f.suptitle('Multiplot')
plt_array[0].plot(sig.InputSignal_1kHz_15kHz)
plt_array[0].set_title("Subplot 01")
plt_array[1].plot(sig.InputSignal_1kHz_15kHz)
plt_array[1].set_title("Subplot 02")
plt_array[2].plot(sig.InputSignal_1kHz_15kHz)
plt_array[2].set_title("Subplot 03")
plt.savefig(os.path.join(OUT_DIR, "Multiplot_InputSignal_1kHz_15kHz"))
