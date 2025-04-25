from dash import Dash, dcc, html, Input, Output
import qrcode
import base64
from io import BytesIO
from datetime import datetime, timezone,timedelta
from qrcode.image.styledpil import StyledPilImage
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="log.csv",level=logging.INFO)
#fh = logging.FileHandler("log.csv")
#logger.addHandler(fh)
#logger.setLevel(logging.DEBUG)

encoded_image = base64.b64encode(open('image.png', 'rb').read())
                         
app = Dash(__name__)

app.layout = html.Div([html.H1(children="QR-CLOCK",id="headline"),
                       html.Div(id="live-update-text"),
                        dcc.Interval(id="update-trigger", interval=1 * 1000, n_intervals=0),
                        html.Img(id="live-update-image",src='')])

@app.callback(
    #Output("update-trigger","interval"),
    Output("live-update-text", "children"),
    Output("live-update-image", "src"),
    Output("update-trigger", "interval"),
    Input('update-trigger',"n_intervals")
    
)
def update_output(n_intervals):
    _start = datetime.now(timezone.utc)
    _dt_strf = _start.strftime(rf"%d/%m/%Y %H:%M:%S %z")
    qr= qrcode.make(_dt_strf,image_factory=StyledPilImage)
    imagefile =BytesIO()   
    qr.save(imagefile,format='png')
    encoded_image = base64.b64encode(imagefile.getvalue())
    src = f'data:image/png;base64,{encoded_image.decode()}'
    _end = datetime.now(timezone.utc)
    _diff = _end - _start
    interval = 1000 -int(_start.microsecond+_diff.microseconds)/1000
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(f"START: {_start} | END: {_end} | Diff: {_diff} | Interval: {interval} | QRCode: {_dt_strf}")
        return [html.H2(children=f"START: {_start.strftime(rf"%d/%m/%Y %H:%M:%S.%f %z")}"),
                html.H2(children=f"END: {_end.strftime(rf"%d/%m/%Y %H:%M:%S.%f %z")}"), 
                html.H3(children=f"CodeExecutionTime: {_diff} [ms]"),
                html.H3(children=f"UpdateIntervalCorrection: {interval} [ms]"),
                html.H3(children=f"QRCode-String: {_dt_strf}"),], src, interval
    else:
        logger.info(f"Interval: {interval} | QRCode: {_dt_strf}")
        return [], src, interval
    
if __name__ == "__main__":
    app.run(debug=False)