from pymusic.models import Song

def create_app():
    try:
        from fastapi import FastAPI
    except ImportError as e: raise RuntimeError("Install pymusic[server]") from e
    app=FastAPI(title="Py-Music API",version="2.0.0")
    @app.get("/health")
    def health(): return {"status":"ok"}
    @app.post("/theory/scale")
    def scale(root:str="C",pattern:str="major"):
        from pymusic.theory import get_scale
        return {"root":root,"pattern":pattern,"notes":get_scale(root,pattern)}
    @app.post("/theory/chord")
    def chord(root:str="C",chord_type:str="major"):
        from pymusic.theory import get_chord
        return {"root":root,"type":chord_type,"notes":get_chord(root,chord_type)}
    return app
app=create_app()
