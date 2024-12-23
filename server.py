from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
import os
import sys

app = FastAPI()

@app.get("/books")
async def serve_book_text(book_name: str):
    file_path = f"./books/{book_name}.txt"
    return FileResponse(file_path)


@app.get("/book_cover")
async def server_book_cover_img(book_name: str) -> FileResponse:
    webp_file_path = f"./book_covers/{book_name}.webp"
    png_file_path = f"./book_covers/{book_name}.png"

    if os.path.exists(webp_file_path):
        return FileResponse(webp_file_path)
    elif os.path.exists(png_file_path):
        return FileResponse(png_file_path)
    else:
        return JSONResponse({"error": "No cover image found for the book"}, status_code=404)

@app.get("/api/v1/list_books")
async def get_list_of_books():
    files = os.listdir("./books")
    data = [file.replace(".txt", "") for file in files if file.endswith(".txt")]
    # sort the list of books alphabetically
    data = sorted(data)
    return JSONResponse(data)



@app.get("/{path:path}")
async def serve_static(path: str):
    if path == "":
        path = "index.html"
    
    return FileResponse(path)


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc == 2:
        port = int(sys.argv[1])
    else:
        port = 8000
    uvicorn.run(app, host="0.0.0.0", port=port)