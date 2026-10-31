"""Host behavior checks; hardware APIs are doubles of PicoWare 2.5's interface."""

import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import Mock, patch


class HelloWorldTests(unittest.TestCase):
    def setUp(self):
        buttons = ModuleType("picoware.system.buttons")
        buttons.BUTTON_BACK = 5
        buttons.BUTTON_ESCAPE = 77
        vector = ModuleType("picoware.system.vector")
        vector.Vector = lambda x, y: (x, y)
        modules = {
            "picoware": ModuleType("picoware"),
            "picoware.system": ModuleType("picoware.system"),
            "picoware.system.buttons": buttons,
            "picoware.system.vector": vector,
        }
        path = Path(__file__).resolve().parents[1] / "apps" / "hello_world.py"
        spec = importlib.util.spec_from_file_location("hello_world", path)
        self.app = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, modules):
            spec.loader.exec_module(self.app)
        self.events = Mock()
        self.input = SimpleNamespace(button=-1, reset=self.events.reset)
        self.manager = SimpleNamespace(
            draw=Mock(spec=["clear", "text", "swap"]),
            input_manager=self.input,
            back=self.events.back,
        )

    def test_start_presents_greeting_before_swapping(self):
        self.assertIs(self.app.start(self.manager), True)
        self.assertEqual(
            self.manager.draw.mock_calls,
            [
                unittest.mock.call.clear(),
                unittest.mock.call.text((24, 136), "Hello, World!"),
                unittest.mock.call.text((24, 168), "Esc / Back to exit"),
                unittest.mock.call.swap(),
            ],
        )

    def test_exit_consumes_event_before_navigating_back(self):
        for button in (5, 77):
            with self.subTest(button=button):
                self.events.reset_mock()
                self.input.button = button
                self.app.run(self.manager)
                self.assertEqual(
                    self.events.mock_calls,
                    [unittest.mock.call.reset(), unittest.mock.call.back()],
                )

    def test_idle_and_other_keys_do_not_exit_or_redraw(self):
        for button in (-1, 0, 4, 7, 74):
            self.input.button = button
            self.app.run(self.manager)
        self.assertEqual(self.events.mock_calls, [])
        self.assertEqual(self.manager.draw.mock_calls, [])

    def test_stop_and_reopen_redraws_greeting(self):
        self.app.start(self.manager)
        self.manager.draw.reset_mock()
        self.app.stop(self.manager)
        self.assertEqual(self.manager.draw.mock_calls, [])
        self.assertIs(self.app.start(self.manager), True)
        self.manager.draw.text.assert_any_call((24, 136), "Hello, World!")
        self.manager.draw.swap.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
