import json
from fastapi import HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, FileResponse


class APIResponse:
    def __init__(self, code, message=None, headers=None, *args, **kwargs):
        self.code = code
        self.message = message
        self.headers = headers

    def http_error(self):
        raise HTTPException(status_code=self.code, detail=self.message, headers=self.headers)
