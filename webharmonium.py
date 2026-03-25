import sys
import os
import tempfile
import threading

# ── Embedded HTML (base64 to avoid multiline quoting issues) ──
import base64

HTML_B64 = None  # filled below

def get_html_path():
    """Write the embedded HTML to a temp file and return its path."""
    html_bytes = base64.b64decode(HTML_B64)
    tmp = tempfile.NamedTemporaryFile(
        delete=False, suffix=".html", prefix="webharmonium_"
    )
    tmp.write(html_bytes)
    tmp.close()
    return tmp.name


def launch_webview(html_path):
    """Try pywebview first, fall back to tkinter + webbrowser."""
    try:
        import webview
        window = webview.create_window(
            "Web Harmonium",
            f"file:///{html_path.replace(os.sep, '/')}",
            width=800,
            height=600,
            resizable=True,
            min_size=(400, 600),
        )
        webview.start()
    except ImportError:
        # Fallback: open in default browser
        import webbrowser
        webbrowser.open(f"file:///{html_path.replace(os.sep, '/')}")
        # Keep process alive with a tiny tkinter window
        try:
            import tkinter as tk
            root = tk.Tk()
            root.title("Web Harmonium")
            root.geometry("280x80")
            root.resizable(False, False)
            lbl = tk.Label(
                root,
                text="Web Harmonium is open in your browser.\nClose this window to quit.",
                font=("Segoe UI", 9),
                pady=16,
            )
            lbl.pack()
            root.mainloop()
        except Exception:
            input("Press Enter to quit…")
    finally:
        try:
            os.unlink(html_path)
        except Exception:
            pass


if __name__ == "__main__":
    # HTML_B64 is injected by build.py before packaging
    if HTML_B64 is None:
        print("ERROR: HTML not embedded. Run build.py to create the .exe")
        sys.exit(1)
    path = get_html_path()
    launch_webview(path)
