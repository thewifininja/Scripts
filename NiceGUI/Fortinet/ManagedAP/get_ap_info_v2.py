from nicegui import ui, app
import requests

# Create The pop-up dialog if Quit is pressed
with ui.dialog() as quit_dialog, ui.card():
	ui.label('Are you sure?')
	with ui.row():
		ui.button('Yes', on_click=app.shutdown)
		ui.button('No', on_click=quit_dialog.close)

def getResults(update_data):
	update_data.clear()
	table_view.update()
	ap_data = fetch_api_data(gate_fqdn, gate_port, gate_apikey)
	if ap_data:
		results = ap_data["results"]
		update_data.extend(results)
		table_view.update()

def fetch_api_data(gate_fqdn, gate_port, gate_apikey):
    url = f"https://{gate_fqdn.value}:{gate_port.value}/api/v2/monitor/wifi/managed_ap"
    headers = {"Authorization": f"Bearer {gate_apikey.value}", "Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        result.set_text("Results: ")
        return response.json()
    except requests.exceptions.RequestException as e:
        result.set_text("Error Fetching Data")
        return None

grid = ui.aggrid({
    'defaultColDef': {'flex': 1},
    'columnDefs': [
        {'headerName': 'serial', 'label': 'Serial', 'field': 'serial', 'align': 'left', 'sortable': True},
		{'headerName': 'board_mac', 'label': 'Base MAC', 'field': 'board_mac', 'align': 'left', 'sortable': True},
		{'headerName': 'name', 'label': 'Name', 'field': 'name', 'align': 'left', 'sortable': True}
    ],
    'rowData': [
        {'serial':'FP231GTF00000001','board_mac':'01:23:45:67:89:10','name':'Example AP Name'}
    ],
    'rowSelection': 'multiple',
}).classes('max-h-40')

ui.markdown("## FortiGate Managed AP Info")
ui.label("FortiGate Details:")
with ui.row():
	gate_fqdn = ui.input(label='FQDN', placeholder='FortiGate FQDN or IP')
	gate_port = ui.input(label='Port', placeholder='HTTPS Port', value="443")
	gate_apikey = ui.input(label='API Key', placeholder='Administrative API Key', password=True, password_toggle_button=True)
with ui.row():
	ui.button("Go", on_click=lambda:getResults(grid["rowData"]))
	ui.button("Quit", on_click=quit_dialog.open)

result = ui.label("")
table_view = ui.table(columns=columns,rows=result_data,row_key='name')


ui.run()