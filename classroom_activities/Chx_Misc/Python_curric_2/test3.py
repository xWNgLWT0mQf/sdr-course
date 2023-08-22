from pcdr.queue_to_waterfall_flowgraph import queue_to_waterfall
from pcdr.gnuradio_misc import configure_and_run_gui_flowgraph
from pcdr import gnuradio_send, ook_modulate, gnuradio_simulate


modulated = ook_modulate([1, 0, 1, 0, 1, 0, 0, 1], bit_length=int(1e6))
gnuradio_simulate(modulated, center_freq=2.413e9, samp_rate=2e6, prepend_zeros=int(8e6))