import traceback
from tkinter import messagebox

from core.logger import app_logger


def handle_exception(error, context="Unexpected application error"):
    """
    Log an exception and show a user-friendly error message.
    """
    error_details = "".join(
        traceback.format_exception(type(error), error, error.__traceback__)
    )

    app_logger.error("%s\n%s", context, error_details)

    messagebox.showerror(
        "Application Error",
        f"{context}\n\nThe error has been logged for review."
    )
