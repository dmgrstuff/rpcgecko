# Building from source

While you can run RPCGecko from a pre-built executable or directly from source with `python rpcgecko.py`, you might want to build an executable yourself. Here are some steps to do just that.

## Requirements

A **non-Microsoft Store** install of the latest [**Python 3.8**](https://python.org/downloads)* release

[**Git**](http://git-scm.com/downloads) is helpful, but isn't strictly required

A computer running the OS you're compiling for (Windows, macOS, or Linux)

*\*Python 3.9 will probably also work as long as you're not using Windows 7.*

---

**1.** First things first, clone the repo with `git clone https://github.com/dmgrstuff/rpcgecko.git && cd rpcgecko`.

If you don't have **Git** or can't install it, you can just [download the .zip](https://github.com/dmgrstuff/rpcgecko/archive/main.zip) and extract it somewhere convenient.

*I'd recommended making a* ***virtual environment*** *before you start to avoid polluting your main Python install with packages you likely won't use in the future. Run `pip install virtualenv` and then `virtualenv venv` to set one up.*

*Switch to the new environment by running `source bin\activate` on Mac or Linux or `.\venv\Scripts\activate.bat (?)` on Windows.*

**2.** Run `pip install pyinstaller`, followed by `pip install requirements.txt`. This installs all the required modules.

**3.** To build the executable as a single file, run `pyinstaller -F rpcgecko.py`. This creates a single `rpcgecko` executable in `\dist\rpcgecko`. It's slower, as necessary files are extracted to a temporary folder before running it, but more portable.

(If you find it too slow and don't care about portability, a faster option would be to build it as a directory with `pyinstaller rpcgecko.py`.)
