import subprocess
import socket
import uvicorn

from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

from models import RackStats
from config import pclist

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


rack_stats = RackStats()


@app.get("/get_data/")
def read_items():
    timestamps, temperatures, humidities = rack_stats.readRecord()
    return JSONResponse({
        "timestamps": timestamps,
        "temperatures": temperatures,
        "humidities": humidities,
        "cur_temperature": temperatures[-1],
        "cur_humidity": humidities[-1],
    })


@app.get("/power-on")
async def power_on(pcId: int):
    payload = address2packet(pclist[pcId]['mac_addr'])
    if payload:
        packet_broadcasting(payload)
    return {"message": f"Power on request received for PC ID: {pcId}"}


@app.get("/get_pc_status/")
async def get_pc_status():
    update_pc_status()
    return JSONResponse({"pclist":pclist})


@app.get("/")
async def index(request: Request):
    update_pc_status()
    return templates.TemplateResponse("index.html", {"request": request, "pclist": pclist})


def update_pc_status():
    global pclist
    for idx, pc in enumerate(pclist):
        pclist[idx]['id'] = idx
        pclist[idx]['status'] = is_host_up(pc['ip'])


def is_host_up(ip):
    command = ['timeout', '0.05', 'ping', '-c', '1', ip]
    response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return response.returncode == 0


def address2packet(address):
    if len(address) == 17:
        separate = address[2]
        address = address.replace(separate, "")
    elif len(address) == 12:
        pass
    else:
        return False

    try:
        bytes_mac = bytes.fromhex("F" * 12 + address *16)
        return bytes_mac
    except ValueError:
        return False


def packet_broadcasting(payload, broadcast_range='255.255.255.255', broadcast_protocol=9):
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
    ret = broadcast_socket.sendto(payload, (broadcast_range, broadcast_protocol))
    print(f'sent [{ret}]byte')
    broadcast_socket.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level='debug', access_log=True)
