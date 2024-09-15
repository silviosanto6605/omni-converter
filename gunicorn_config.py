import os
import multiprocessing



workers = multiprocessing.cpu_count() * 2 + 1
bind = "0.0.0.0:8080"
threads = 4
timeout = 120