# SPDX-License-Identifier: MIT
from datetime import datetime
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest
spec=importlib.util.spec_from_file_location('dashboard',Path(__file__).resolve().parents[1]/'companion/dashboard.py')
dashboard=importlib.util.module_from_spec(spec);spec.loader.exec_module(dashboard)

class CompanionTests(unittest.TestCase):
    def metrics(self,battery):
        return SimpleNamespace(cpu_percent=lambda interval:42.8,
            virtual_memory=lambda:SimpleNamespace(percent=61.2),sensors_battery=lambda:battery)
    def test_packet(self):
        m=self.metrics(SimpleNamespace(percent=87.4,power_plugged=True))
        self.assertEqual(dashboard.sample(m,datetime(2026,11,4,17,45,29)),
            b'DASH 17:45:29 2026-11-04 428 612 87 1\n')
    def test_no_host_battery(self):
        self.assertTrue(dashboard.sample(self.metrics(None)).endswith(b' -1 0\n'))
    def test_identity(self):
        class Port:
            def reset_input_buffer(self): pass
            def write(self,b): self.sent=b
            def readline(self,n): return self.response
        p=Port();p.response=b'{"device":"desk-fidget-counter","protocol":1}\n'
        self.assertTrue(dashboard.identify(p));self.assertEqual(p.sent,b'\nSTATUS\n')
        p.response=b'{"device":"another-device","protocol":1}\n'
        self.assertFalse(dashboard.identify(p))
    def test_nonfinite(self):
        with self.assertRaises(ValueError): dashboard.tenths(float('nan'))

if __name__=='__main__': unittest.main()
