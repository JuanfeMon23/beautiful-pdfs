from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel, Field
from typing import List, Union, Optional
from weasyprint import HTML, CSS
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DataRequest(BaseModel):
    time: Union[float, int]
    heart_rate: Union[float, int]
    PseBorg: Optional[Union[float, int]] = Field(default=None)
    oxygen: Union[float, int]
    target: Union[float, int]

@app.post("/generate-pdf", response_class=Response)
async def generate_pdf(data: List[DataRequest]):
    try:
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>PDF with Dynamic Data</title>
            <style>
                @page {{
                    size: A4;
                    margin: 20mm;
                }}

                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                }}

                .content {{
                    page-break-before: auto;
                    page-break-after: auto;
                }}

                h1 {{
                    text-align: center;
                }}

                p {{
                    text-align: justify;
                }}

                table {{
                    width: 70%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}

                table, th, td {{
                    border: 1px solid black;
                    border-radius : 8px;
                }}

                th, td {{
                    padding: 10px;
                    text-align: left;
                }}
            </style>
        </head>
        <body>
            <header>
                <h1>Test de esfuerzo</h1>
            </header>
            <main class="content">
                <table>
                    <thead>
                        <tr>
                            <td>Etapa</td>
                            <td>Tiempo[s]</td>
                            <td>Rf[bpm]</td>
                            <td>PSE Borg</td>
                            <td>VO2</td>
                            <td>Target[W]</td>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join(f"<tr><td>{index + 1}</td><td>{item.time}</td><td>{item.heart_rate}</td><td>{item.PseBorg}</td><td>{item.oxygen}</td><td>{item.target}</td></tr>" for index, item in enumerate(data))}
                    </tbody>
                </table>
            </main>
        </body>
        </html>
        """
        pdf = HTML(string=html_content).write_pdf()

        return Response(content=pdf, media_type="applic ation/pdf", headers={
            "Content-Disposition": "inline; filename=dynamic_data.pdf"
        })
    except Exception as e:

        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
