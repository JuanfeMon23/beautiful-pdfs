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


class PretestData(BaseModel):
    isPositive : str
    yearsOfBirthday: str
    restFc: str
    maximumFc: str
    cardiovascularSynthm: str
    bloodPresure: str
    cardiovascularAuscultation: str
    pulmonarAuscultation: str
    initialRysk: str
    initialOmRisk: str
    generalMovility: str
    observations: str

class EffortTestData(BaseModel):
    time: Union[float, int]
    heart_rate: Union[float, int]
    PseBorg: Optional[Union[float, int]] = Field(default='')
    oxygen: Union[float, int]
    target: Union[float, int]

class DataRequest(BaseModel):
    data: List[EffortTestData]
    items: List[str]
    pretestData : PretestData
    pretestRecomendations : List[str]

@app.post("/generate-pdf", response_class=Response)
async def generate_pdf(data: DataRequest):
    print(data)
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

                .table_title {{
                    font-weight: bold;
                    text-decoration: underline;
                }}

                .observation_place {{
                  text-align: justify;
                    text-justify: inter-word;
                    width: 80%;
                }}
            </style>
        </head>
        <body>
            <p class="table_title">Tabla    resultados obtenidos en el pretest fisico</p>
            <table>
                <thead>
                    <tr>
                        <td>Variable</td>
                        <td>Resultado</td>
                    </tr>
                </thead>
<tbody>
                    <tr>
                        <td>Cumple requisitos</td>
                        <td>{data.pretestData.isPositive}</td>
                    </tr>
                    <tr>
                        <td>Edad (años)</td>
                        <td>{data.pretestData.yearsOfBirthday}</td>
                    </tr>
                    <tr>
                        <td>FC en reposo (l.p.m)</td>
                        <td>{data.pretestData.restFc}</td>
                    </tr>
                    <tr>
                        <td>FC máxima teórica [207 - (edad * 0.7)]</td>
                        <td>{data.pretestData.maximumFc}</td>
                    </tr>
                    <tr>
                        <td>Síntomas cardiovasculares actuales</td>
                        <td>{data.pretestData.cardiovascularSynthm}</td>
                    </tr>
                    <tr>
                        <td>Presión arterial inicial (mmHg)</td>
                        <td>{data.pretestData.bloodPresure}</td>
                    </tr>
                    <tr>
                        <td>Auscultación cardiovascular</td>
                        <td>{data.pretestData.cardiovascularAuscultation}</td>
                    </tr>
                    <tr>
                        <td>Auscultación pulmonar</td>
                        <td>{data.pretestData.pulmonarAuscultation}</td>
                    </tr>
                    <tr>
                        <td>Movilidad general</td>
                        <td>{data.pretestData.generalMovility}</td>
                    </tr>
                    <tr>
                        <td>Observaciones</td>
                        <td>{data.pretestData.observations}</td>
                    </tr>
                    <tr>
                        <td>RCV</td>
                        <td>{data.pretestData.initialRysk}</td>
                    </tr>
                    <tr>
                        <td>Riesgo OM inicial</td>
                        <td>{data.pretestData.initialOmRisk}</td>
                    </tr>
                </tbody>
            </table>
            <div class="observation_place">
                <h4>Recomendaciones</h4>
                        {"".join(f"<li>{item}</li>" for index, item in enumerate(data.pretestRecomendations))}
            </div>
            <p class="table_title">Tabla resultados test consumo maximo de oxigeno en bicicleta</p>
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
                        {"".join(f"<tr><td>{index + 1}</td><td>{item.time}</td><td>{item.heart_rate}</td><td>{item.PseBorg}</td><td>{item.oxygen}</td><td>{item.target}</td></tr>" for index, item in enumerate(data.data))}
                    </tbody>
                </table>
                <div class="observation_place">
                    <h4>Observaciones</h4>
                            {"".join(f"<li>{item}</li>" for index, item in enumerate(data.items))}
                </div>
            </main>
        </body>
        </html>
        """
        pdf = HTML(string=html_content).write_pdf()

        return Response(content=pdf, media_type="application/pdf", headers={
            "Content-Disposition": "inline; filename=dynamic_data.pdf"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
