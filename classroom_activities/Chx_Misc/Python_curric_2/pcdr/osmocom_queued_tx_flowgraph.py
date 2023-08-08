#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Osmocom helper
# GNU Radio version: 3.8.1.0

import numpy as np
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio import blocks
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time
from queue import SimpleQueue
from typing import Optional



class __print_blk(gr.sync_block):

    def __init__(self, sleep_seconds=0.5):
        gr.sync_block.__init__(
            self,
            name="Python Block: Print",
            in_sig=[np.complex64],
            out_sig=[]
        )
        self.sleep_seconds = sleep_seconds
        
    def work(self, input_items, output_items):
        singleDataPoint = input_items[0][0]

        print(singleDataPoint)
        time.sleep(self.sleep_seconds)

        return 1


class __string_file_sink(gr.sync_block):

    def __init__(self, filename):
        gr.sync_block.__init__(
            self,
            name="Python Block: String File Sink",
            in_sig=[np.complex64],
            out_sig=[]
        )
        self.f = open(filename, "w")
        
    def work(self, input_items, output_items):
        singleDataPoint = input_items[0][0]

        self.f.write(f"{singleDataPoint}, ")
        self.f.flush()

        return 1


class __data_queue_source(gr.sync_block):

    def __init__(self, external_queue: SimpleQueue, chunk_size: int):
        gr.sync_block.__init__(
            self,
            name='Python Block: Data Queue Source',
            in_sig=[],
            out_sig=[(np.complex64, chunk_size)]
        )
        self.__data_queue = external_queue
        self._chunk_size = chunk_size

    def work(self, input_items, output_items):
        output_items[0][0] = self.__data_queue.get()
        return 1
    
    def queue_put(self, data):
        if len(data) != self._chunk_size:
            raise ValueError(f"Data must be {self._chunk_size} items long")
        self.__data_queue.put(data)


## Bizarre GNU Radio variable-rename issues

_queue_to__print_blk__data_queue_source = __data_queue_source
_queue_to__string_file_sink__data_queue_source = __data_queue_source
_queue_to__osmocom_sink__data_queue_source = __data_queue_source
_queue_to__string_file_sink__string_file_sink = __string_file_sink
_queue_to__print_blk__print_blk = __print_blk

class queue_to__osmocom_sink(gr.top_block):

    def __init__(self,
                 center_freq: float,
                 samp_rate: float,
                 chunk_size: int,
                 if_gain: int,
                 external_queue: SimpleQueue):
        
        gr.top_block.__init__(self, "Top block")

        self.samp_rate = samp_rate
        
        self.data_queue_source = __data_queue_source(external_queue, chunk_size)

        self.vector_to_stream = blocks.vector_to_stream(gr.sizeof_gr_complex, chunk_size)

        self.osmosdr_sink = osmosdr.sink()
        self.osmosdr_sink.set_sample_rate(samp_rate)
        self.osmosdr_sink.set_center_freq(center_freq)
        self.osmosdr_sink.set_gain(0)
        self.osmosdr_sink.set_if_gain(if_gain)
        self.osmosdr_sink.set_bb_gain(0)

        self.connect(self.data_queue_source, self.vector_to_stream, self.osmosdr_sink)


class queue_to__print_blk(gr.top_block):

    def __init__(self, print_delay: float, external_queue: SimpleQueue, chunk_size: int):
        gr.top_block.__init__(self, "Top block")
        self.data_queue_source = __data_queue_source(external_queue, chunk_size)
        self.vector_to_stream = blocks.vector_to_stream(gr.sizeof_gr_complex, chunk_size)
        self.print_blk = __print_blk(print_delay)
        self.connect(self.data_queue_source, self.vector_to_stream, self.print_blk)


class queue_to__string_file_sink(gr.top_block):

    def __init__(self, filename: str, external_queue: SimpleQueue, chunk_size: int):
        gr.top_block.__init__(self, "Top block")
        self.data_queue_source = __data_queue_source(external_queue, chunk_size)
        self.vector_to_stream = blocks.vector_to_stream(gr.sizeof_gr_complex, chunk_size)
        self.string_file_sink = __string_file_sink(filename)
        self.connect(self.data_queue_source, self.vector_to_stream, self.string_file_sink)


class top_block_manager():

    def __init__(self, tb):
        self.tb = tb
        def sig_handler(sig=None, frame=None):
            tb.stop()
            tb.wait()
            sys.exit(0)

        signal.signal(signal.SIGINT, sig_handler)
        signal.signal(signal.SIGTERM, sig_handler)

    def start(self):
        self.tb.start()    
    
    def start_and_keep_open(self, seconds: float):
        self.start()
        time.sleep(seconds)