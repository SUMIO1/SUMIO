import logging
import os
import sys

from kivy.lang import Builder
from kivy.resources import resource_add_path

from src.app.gui.app import SumioApp

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

KV_TEMPLATES_DIR_PREFIX = "app/kv_templates"

if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        # print(os.path.join(sys._MEIPASS))
        resource_add_path(os.path.join(sys._MEIPASS))
        kv_templates_dir = os.path.join(sys._MEIPASS, KV_TEMPLATES_DIR_PREFIX)
    else:
        kv_templates_dir = os.path.join(os.path.curdir, KV_TEMPLATES_DIR_PREFIX)

    # print(os.listdir(kv_templates_dir))

    kv_paths = [os.path.join(kv_templates_dir, f) for f in os.listdir(kv_templates_dir)]
    kv_file_paths = [f for f in kv_paths if os.path.isfile(f)]
    # print(kv_file_paths)

    for kv_file_path in kv_file_paths:
        Builder.load_file(kv_file_path)

    SumioApp().run()
