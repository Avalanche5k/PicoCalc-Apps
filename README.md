# PicoCalc-Apps

Custom MicroPython applications for the ClockworkPi PicoCalc with a Raspberry Pi
Pico 2 W running jblanked's **PicoWare 2.5.0**.

## Hello World

[`apps/hello_world.py`](apps/hello_world.py) displays **Hello, World!** and an exit
hint. Press **Esc** or PicoWare's configured **Back** key to return to the Custom
applications menu. No Wi-Fi, extra libraries, or compilation is required.

### Installation

1. Start with PicoWare **MicroPython 2.5.0** installed for the **PicoCalc Pico 2 W**
   (upstream firmware: `builds/MicroPython/Picoware-PicoCalcPico2W.uf2`). This app
   uses PicoWare's bundled modules and does not run on plain MicroPython alone.
2. Shut down the PicoCalc and insert its SD card into your computer.
3. Create `picoware/apps` at the root of that SD card if it does not exist. Copy
   `apps/hello_world.py` from this repository there, keeping the filename:

   ```text
   <SD card root>/picoware/apps/hello_world.py
   ```

   PicoWare mounts this as `/sd/picoware/apps/hello_world.py`. Do not copy it into
   the firmware's internal `picoware` package or replace `main.py`.
4. Safely eject the card, put it back into the PicoCalc, and boot PicoWare.
5. Open **Applications → Custom**, select **hello_world**, and press Enter.
   The loader displays the filename without `.py` as the menu label.
6. Check that the greeting appears, then press Esc / Back. Verify the Custom menu
   returns and that you can open the application again.

If the app is missing, check the SD card path and reopen the Custom menu. Avoid
keeping a stale `hello_world.mpy` alongside the source file.

### Verified upstream interface

The implementation was checked against jblanked/PicoWare tag
[`v2.5.0`](https://github.com/jblanked/PicoWare/tree/v2.5.0), commit
`566d2e59982091e3ae90f7a7bb5fc644ecf162c0`, before writing the app:

- [AppLoader](https://github.com/jblanked/PicoWare/blob/v2.5.0/src/MicroPython/picoware/system/app_loader.py)
  discovers `.py` / `.mpy` files in `/picoware/apps` on storage and requires callable
  `start(view_manager)`, `run(view_manager)`, and `stop(view_manager)` functions.
- [Custom applications](https://github.com/jblanked/PicoWare/blob/v2.5.0/src/MicroPython/picoware/applications/applications/custom.py)
  wraps these callbacks in a managed View; `start` must return `True`. PicoWare
  calls `run` each frame, so the application needs no private event loop.
- [hello_color example](https://github.com/jblanked/PicoWare/blob/v2.5.0/builds/MicroPython/apps_unfrozen/hello_color.py)
  uses `draw.clear()`, `draw.text(Vector(x, y), text)`, `draw.swap()`, input reset,
  and `view_manager.back()`. Hello World follows the same pattern.
- [Input mapping](https://github.com/jblanked/PicoWare/blob/v2.5.0/src/MicroPython/picoware/system/input.py)
  maps Escape according to the configured exit button. The app accepts both
  `BUTTON_ESCAPE` and `BUTTON_BACK`.

### Development checks

Run the host-side behavior tests with Python 3:

```sh
python3 -m unittest discover -s tests -v
```

These tests replace hardware-facing modules with test doubles. They check drawing,
input handling, and reopening; they do not emulate the LCD, keyboard, SD card, or
MicroPython firmware. The installation steps above include the on-device smoke
check; physical hardware validation remains required.
